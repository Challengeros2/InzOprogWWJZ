"""Wirgo v1: a local Flask API for the existing browser interface."""
from __future__ import annotations

from datetime import datetime

from flask import Flask, jsonify, request

import database
from controllers.api import bp as public_bp
from models.wirgo import wristband, attraction, order_data

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
# P3 F01: tworzenie opasek przeniesiono do kontrolera i modelu.
# Pozostale funkcje sa nadal w tym pliku do kolejnych krokow.


@app.post('/api/wristbands/<band_id>/recharge')
def recharge(band_id):
    """F02: check and top-up an existing token wristband."""
    amount = positive_int((request.get_json(silent=True) or {}).get('amount'), 10000)
    if amount is None:
        return error('Doładowanie musi być dodatnią liczbą całkowitą.')
    with database.transaction() as db:
        row = db.execute('SELECT * FROM opaska WHERE id=?', (band_id.upper(),)).fetchone()
        if not row:
            return error('Nie znaleziono opaski.', 404)
        if row['typ'] != 'tokens':
            return error('Nie można doładować karnetu czasowego.')
        db.execute('UPDATE opaska SET zetony=zetony+? WHERE id=?', (amount, row['id']))
        updated = db.execute('SELECT * FROM opaska WHERE id=?', (row['id'],)).fetchone()
    return jsonify({'wristband': wristband(updated)})


@app.get('/api/wristbands/<band_id>')
def get_wristband(band_id):
    with database.connect() as db:
        row = db.execute('SELECT * FROM opaska WHERE id=?', (band_id.upper(),)).fetchone()
        if not row:
            return error('Nie znaleziono opaski.', 404)
        return jsonify({'wristband': wristband(row)})


@app.post('/api/orders')
def new_order():
    """F03: save a food order with its product rows and calculated total."""
    items = (request.get_json(silent=True) or {}).get('items')
    if not isinstance(items, list) or not items or len(items) > 30:
        return error('Zamówienie musi zawierać co najmniej jeden produkt.')
    with database.transaction() as db:
        validated, total = [], 0
        for item in items:
            if not isinstance(item, dict):
                return error('Niepoprawna pozycja zamówienia.')
            product = db.execute('SELECT * FROM produkt WHERE id=?', (item.get('id'),)).fetchone()
            qty = positive_int(item.get('qty'), 100)
            if not product or qty is None:
                return error('Nieznany produkt lub niepoprawna ilość.')
            validated.append((product['id'], qty, product['cena_grosze']))
            total += qty * product['cena_grosze']
        now = datetime.now().isoformat(timespec='seconds')
        cursor = db.execute('INSERT INTO zamowienie(status,utworzono,suma_grosze) VALUES(?,?,?)',
                            ('Oczekujące', now, total))
        order_id = cursor.lastrowid
        db.executemany('INSERT INTO pozycja_zamowienia(zamowienie_id,produkt_id,ilosc,cena_grosze) '
                       'VALUES(?,?,?,?)', [(order_id, *item) for item in validated])
        row = db.execute('SELECT * FROM zamowienie WHERE id=?', (order_id,)).fetchone()
        order = order_data(db, row)
    return jsonify({'order': order}), 201


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
