"""Wirgo v1: a local Flask API for the existing browser interface."""
from __future__ import annotations

from datetime import datetime

from flask import Flask, jsonify, request

import database
from controllers.api import bp as public_bp
from models.wirgo import attraction

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(public_bp)

VALID_STATUSES = {'Działająca', 'Uszkodzona', 'W trakcie naprawy', 'Zamknięta'}
ORDER_STATUSES = {'Oczekujące', 'W trakcie', 'Zrealizowane', 'Nieodebrane'}


def error(message, status=400):
    return jsonify({'error': message}), status


def positive_int(value, maximum=100000):
    """Reject empty, nonintegers, zero, negatives and huge numbers."""
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, str)) or str(value).strip() != str(value):
        return None
    try:
        number = int(value)
    except (ValueError, TypeError):
        return None
    return number if str(number) == str(value) and 1 <= number <= maximum else None


# P2: strona glowna i /api/state sa w controllers/api.py.
# P3 F01, F02, F03: obsluga opasek i zamowien gastronomicznych jest w MVC.
# F05, F06 i opcjonalna obsluga kuchni pozostaja na razie w app.py.


@app.patch('/api/orders/<int:order_id>/status')
def update_order_status(order_id):
    """Optional prototype support for the kitchen (planned for v2)."""
    status = (request.get_json(silent=True) or {}).get('status')
    if status not in ORDER_STATUSES:
        return error('Nieznany status zamówienia.')
    with database.transaction() as db:
        row = db.execute('SELECT id FROM zamowienie WHERE id=?', (order_id,)).fetchone()
        if not row:
            return error('Nie znaleziono zamówienia.', 404)
        db.execute('UPDATE zamowienie SET status=? WHERE id=?', (status, order_id))
    return jsonify({'status': status})


@app.patch('/api/attractions/<int:attraction_id>/status')
def change_attraction(attraction_id):
    """F05: update attraction status; gate uses the same stored status."""
    status = (request.get_json(silent=True) or {}).get('status')
    if status not in VALID_STATUSES:
        return error('Nieznany status atrakcji.')
    with database.transaction() as db:
        row = db.execute('SELECT * FROM atrakcja WHERE id=?', (attraction_id,)).fetchone()
        if not row:
            return error('Nie znaleziono atrakcji.', 404)
        db.execute('UPDATE atrakcja SET status=? WHERE id=?', (status, attraction_id))
        row = db.execute('SELECT * FROM atrakcja WHERE id=?', (attraction_id,)).fetchone()
    return jsonify({'attraction': attraction(row)})


@app.post('/api/entry')
def verify_entry():
    """F06: check admission and deduct tokens atomically if allowed."""
    body = request.get_json(silent=True) or {}
    band_id = str(body.get('wristband_id') or '').strip().upper()
    attr_id = positive_int(body.get('attraction_id'), 100000)
    if not band_id or attr_id is None:
        return error('Podaj identyfikator opaski i wybierz atrakcję.')
    with database.transaction() as db:
        attr = db.execute('SELECT * FROM atrakcja WHERE id=?', (attr_id,)).fetchone()
        if not attr:
            return error('Nie znaleziono atrakcji.', 404)
        if attr['status'] != 'Działająca':
            return jsonify({'allowed': False, 'reason': 'attraction_closed',
                            'message': f"Atrakcja jest niedostępna: {attr['status']}"})
        band = db.execute('SELECT * FROM opaska WHERE id=?', (band_id,)).fetchone()
        if not band:
            return jsonify({'allowed': False, 'reason': 'unknown_wristband',
                            'message': f'Nieznana opaska {band_id}.'})
        cost = 0
        if band['typ'] == 'pass':
            if not band['wazna_do'] or datetime.fromisoformat(band['wazna_do']) <= datetime.now():
                return jsonify({'allowed': False, 'reason': 'expired', 'message': 'Karnet stracił ważność.'})
        else:
            cost = attr['koszt']
            if band['zetony'] < cost:
                return jsonify({'allowed': False, 'reason': 'not_enough_tokens',
                                'message': f"Brak żetonów: wymagane {cost}, dostępne {band['zetony']}."})
            db.execute('UPDATE opaska SET zetony=zetony-? WHERE id=?', (cost, band_id))
        db.execute('INSERT INTO wejscie(opaska_id,atrakcja_id,koszt_zetonow,czas) VALUES(?,?,?,?)',
                   (band_id, attr_id, cost, datetime.now().isoformat(timespec='seconds')))
        remaining = band['zetony'] - cost if band['typ'] == 'tokens' else None
        return jsonify({'allowed': True, 'reason': 'ok', 'message': 'Zezwolono na wejście.',
                        'wristband_id': band_id, 'owner': band['wlasciciel'],
                        'type': band['typ'], 'attraction': attr['nazwa'],
                        'deducted': cost, 'remaining': remaining})


if __name__ == '__main__':
    app.run(debug=True)
