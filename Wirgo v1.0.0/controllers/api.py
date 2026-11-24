"""P2: kontrole HTTP dla strony głównej i pobierania danych początkowych."""
from flask import Blueprint, jsonify, render_template, request

from models.wirgo import (load_state, issue_wristband, read_wristband,
                          top_up_wristband, create_food_order, change_attraction_status,
                          verify_attraction_entry, InputError, NotFoundError)

bp = Blueprint('public', __name__)


@bp.get('/')
def index():
    return render_template('index.html')


@bp.get('/api/state')
def get_state():
    return jsonify(load_state())


@bp.post('/api/wristbands')
def create_wristband():
    """F01: odbiera formularz i przekazuje operacje do modelu."""
    body = request.get_json(silent=True) or {}
    try:
        band = issue_wristband(body)
    except InputError as exc:
        return jsonify({'error': str(exc)}), 400
    return jsonify({'wristband': band}), 201


@bp.get('/api/wristbands/<band_id>')
def get_wristband(band_id):
    """F02: HTTP -> odczyt opaski z modelu."""
    try:
        band = read_wristband(band_id)
    except NotFoundError as exc:
        return jsonify({'error': str(exc)}), 404
    return jsonify({'wristband': band})


@bp.post('/api/wristbands/<band_id>/recharge')
def recharge(band_id):
    """F02: HTTP -> sprawdzenie i doladowanie w modelu."""
    body = request.get_json(silent=True) or {}
    try:
        band = top_up_wristband(band_id, body.get('amount'))
    except NotFoundError as exc:
        return jsonify({'error': str(exc)}), 404
    except InputError as exc:
        return jsonify({'error': str(exc)}), 400
    return jsonify({'wristband': band})


@bp.post('/api/orders')
def new_order():
    """F03: HTTP -> model zapisujacy zamowienie."""
    body = request.get_json(silent=True) or {}
    try:
        order = create_food_order(body.get('items'))
    except InputError as exc:
        return jsonify({'error': str(exc)}), 400
    return jsonify({'order': order}), 201


@bp.patch('/api/attractions/<int:attraction_id>/status')
def change_attraction(attraction_id):
    """F05: kontroler przekazuje zmiane statusu do modelu."""
    body = request.get_json(silent=True) or {}
    try:
        updated = change_attraction_status(attraction_id, body.get('status'))
    except NotFoundError as exc:
        return jsonify({'error': str(exc)}), 404
    except InputError as exc:
        return jsonify({'error': str(exc)}), 400
    return jsonify({'attraction': updated})


@bp.post('/api/entry')
def verify_entry():
    """F06: przekaz odczyt identyfikatora do modelu i zwroc wynik bramki."""
    body = request.get_json(silent=True) or {}
    try:
        result = verify_attraction_entry(body.get('wristband_id'), body.get('attraction_id'))
    except NotFoundError as exc:
        return jsonify({'error': str(exc)}), 404
    except InputError as exc:
        return jsonify({'error': str(exc)}), 400
    return jsonify(result)
