"""P2: kontrole HTTP dla strony głównej i pobierania danych początkowych."""
from flask import Blueprint, jsonify, render_template

from models.wirgo import load_state

bp = Blueprint('public', __name__)


@bp.get('/')
def index():
    return render_template('index.html')


@bp.get('/api/state')
def get_state():
    return jsonify(load_state())
