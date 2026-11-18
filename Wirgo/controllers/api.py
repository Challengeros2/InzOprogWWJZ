"""P2: kontrole HTTP dla strony głównej i pobierania danych początkowych."""
from flask import Blueprint, jsonify, render_template, request

from models.wirgo import load_state, issue_wristband, InputError

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
