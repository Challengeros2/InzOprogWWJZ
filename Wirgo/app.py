"""Wirgo v1: a local Flask API for the existing browser interface."""
from __future__ import annotations

from flask import Flask, jsonify, request

import database
from controllers.api import bp as public_bp

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(public_bp)

ORDER_STATUSES = {'Oczekujące', 'W trakcie', 'Zrealizowane', 'Nieodebrane'}


def error(message, status=400):
    return jsonify({'error': message}), status


# P2: strona glowna i /api/state sa w controllers/api.py.
# P3: wszystkie funkcje MVP F01, F02, F03, F05 i F06 sa w MVC.
# Dodatkowy ekran kuchni (v2/demo) nadal obslugiwany w app.py.


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


if __name__ == '__main__':
    app.run(debug=True)
