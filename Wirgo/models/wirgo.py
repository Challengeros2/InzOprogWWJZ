"""Model Wirgo: dane poczatkowe i logika F01.

Pozostale funkcje zostana przeniesione osobno w kolejnych krokach P3.
"""
from datetime import datetime, timedelta
import database


def wristband(row):
    return {'id': row['id'], 'type': row['typ'], 'balance': row['zetony'],
            'owner': row['wlasciciel'], 'valid_until': row['wazna_do']}


def attraction(row):
    return {'id': row['id'], 'name': row['nazwa'], 'cost': row['koszt'], 'status': row['status']}


def order_data(db, row):
    items = db.execute('''SELECT p.nazwa AS name, poz.ilosc AS qty
                          FROM pozycja_zamowienia poz
                          JOIN produkt p ON poz.produkt_id=p.id
                          WHERE poz.zamowienie_id=? ORDER BY poz.id''', (row['id'],)).fetchall()
    return {'id': row['id'], 'items': [dict(item) for item in items],
            'status': row['status'], 'time': row['utworzono'][11:16],
            'total': row['suma_grosze'] / 100}



def load_state():
    """Pobierz aktualny stan z SQLite. Bez odpowiedzi HTTP i kodu Flask."""
    with database.connect() as db:
        bands = db.execute('SELECT * FROM opaska ORDER BY id').fetchall()
        attrs = db.execute('SELECT * FROM atrakcja ORDER BY id').fetchall()
        orders = db.execute('SELECT * FROM zamowienie ORDER BY id DESC').fetchall()
        products = db.execute('SELECT * FROM produkt ORDER BY id').fetchall()
        return {
            'wristbands': {row['id']: wristband(row) for row in bands},
            'attractions': [attraction(row) for row in attrs],
            'orders': [order_data(db, row) for row in orders],
            'menu': [{'id': r['id'], 'name': r['nazwa'], 'price': r['cena_grosze'] / 100,
                      'icon': r['ikona']} for r in products],
        }


class InputError(ValueError):
    """Niepoprawne dane od uzytkownika (HTTP 400 w kontrolerze)."""


def _positive_int(value, maximum):
    """Dopuszcza tylko dodatnie liczby calkowite w okreslonym zakresie."""
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, str)) or str(value).strip() != str(value):
        return None
    try:
        number = int(value)
    except (ValueError, TypeError):
        return None
    return number if str(number) == str(value) and 1 <= number <= maximum else None


def issue_wristband(body):
    """F01: sprawdz dane i zapisz nowa opaske do SQLite. Bez kodu Flask."""
    if not isinstance(body, dict):
        raise InputError('Wybierz rodzaj wejściówki.')
    kind = body.get('type')
    if kind not in ('tokens', 'pass'):
        raise InputError('Wybierz rodzaj wejściówki.')

    balance, expiry = 0, None
    if kind == 'tokens':
        balance = _positive_int(body.get('tokens'), 10000)
        if balance is None:
            raise InputError('Liczba żetonów musi być dodatnią liczbą całkowitą.')
    else:
        days = _positive_int(body.get('days'), 7)
        if days not in (1, 3, 7):
            raise InputError('Dostępne karnety: 1, 3 lub 7 dni.')
        expiry = (datetime.now() + timedelta(days=days)).isoformat(timespec='seconds')

    owner = str(body.get('owner') or 'Gość').strip()[:80] or 'Gość'
    with database.transaction() as db:
        next_id = db.execute(
            "SELECT COALESCE(MAX(CAST(SUBSTR(id,5) AS INTEGER)),0)+1 FROM opaska"
        ).fetchone()[0]
        band_id = f'PAS-{next_id:03d}'
        db.execute(
            'INSERT INTO opaska(id,typ,zetony,wazna_do,wlasciciel,utworzono) VALUES(?,?,?,?,?,?)',
            (band_id, kind, balance, expiry, owner, datetime.now().isoformat(timespec='seconds'))
        )
        row = db.execute('SELECT * FROM opaska WHERE id=?', (band_id,)).fetchone()
    return wristband(row)
