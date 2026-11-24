"""Model Wirgo: dane poczatkowe i logika F01, F02, F03, F05 i F06.

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


class NotFoundError(LookupError):
    """Brak wskazanego rekordu (HTTP 404 w kontrolerze)."""


def read_wristband(band_id):
    """F02: odczytaj stan opaski z SQLite. Bez kodu Flask."""
    with database.connect() as db:
        row = db.execute('SELECT * FROM opaska WHERE id=?', (band_id.upper(),)).fetchone()
    if row is None:
        raise NotFoundError('Nie znaleziono opaski.')
    return wristband(row)


def top_up_wristband(band_id, amount):
    """F02: zweryfikuj kwote i zwieksz saldo opaski zetonowej."""
    amount = _positive_int(amount, 10000)
    if amount is None:
        raise InputError('Doładowanie musi być dodatnią liczbą całkowitą.')
    with database.transaction() as db:
        row = db.execute('SELECT * FROM opaska WHERE id=?', (band_id.upper(),)).fetchone()
        if row is None:
            raise NotFoundError('Nie znaleziono opaski.')
        if row['typ'] != 'tokens':
            raise InputError('Nie można doładować karnetu czasowego.')
        db.execute('UPDATE opaska SET zetony=zetony+? WHERE id=?', (amount, row['id']))
        updated = db.execute('SELECT * FROM opaska WHERE id=?', (row['id'],)).fetchone()
    return wristband(updated)


def create_food_order(items):
    """F03: zweryfikuj pozycje i zapisz cale zamowienie w jednej transakcji."""
    if not isinstance(items, list) or not items or len(items) > 30:
        raise InputError('Zamówienie musi zawierać co najmniej jeden produkt.')
    with database.transaction() as db:
        validated, total = [], 0
        for item in items:
            if not isinstance(item, dict):
                raise InputError('Niepoprawna pozycja zamówienia.')
            product = db.execute('SELECT * FROM produkt WHERE id=?', (item.get('id'),)).fetchone()
            qty = _positive_int(item.get('qty'), 100)
            if not product or qty is None:
                raise InputError('Nieznany produkt lub niepoprawna ilość.')
            validated.append((product['id'], qty, product['cena_grosze']))
            total += qty * product['cena_grosze']
        now = datetime.now().isoformat(timespec='seconds')
        cursor = db.execute(
            'INSERT INTO zamowienie(status,utworzono,suma_grosze) VALUES(?,?,?)',
            ('Oczekujące', now, total)
        )
        order_id = cursor.lastrowid
        db.executemany(
            'INSERT INTO pozycja_zamowienia(zamowienie_id,produkt_id,ilosc,cena_grosze) '
            'VALUES(?,?,?,?)', [(order_id, *item) for item in validated]
        )
        row = db.execute('SELECT * FROM zamowienie WHERE id=?', (order_id,)).fetchone()
        order = order_data(db, row)
    return order


VALID_ATTRACTION_STATUSES = {'Działająca', 'Uszkodzona', 'W trakcie naprawy', 'Zamknięta'}


def change_attraction_status(attraction_id, status):
    """F05: zmien status w SQLite i zwroc aktualne dane atrakcji."""
    if status not in VALID_ATTRACTION_STATUSES:
        raise InputError('Nieznany status atrakcji.')
    with database.transaction() as db:
        row = db.execute('SELECT * FROM atrakcja WHERE id=?', (attraction_id,)).fetchone()
        if row is None:
            raise NotFoundError('Nie znaleziono atrakcji.')
        db.execute('UPDATE atrakcja SET status=? WHERE id=?', (status, attraction_id))
        updated = db.execute('SELECT * FROM atrakcja WHERE id=?', (attraction_id,)).fetchone()
    return attraction(updated)


def verify_attraction_entry(wristband_id, attraction_id):
    """F06: sprawdz wstep i pobierz zetony w jednej transakcji SQLite."""
    band_id = str(wristband_id or '').strip().upper()
    attr_id = _positive_int(attraction_id, 100000)
    if not band_id or attr_id is None:
        raise InputError('Podaj identyfikator opaski i wybierz atrakcję.')

    with database.transaction() as db:
        attr = db.execute('SELECT * FROM atrakcja WHERE id=?', (attr_id,)).fetchone()
        if attr is None:
            raise NotFoundError('Nie znaleziono atrakcji.')
        if attr['status'] != 'Działająca':
            return {'allowed': False, 'reason': 'attraction_closed',
                    'message': f"Atrakcja jest niedostępna: {attr['status']}"}

        band = db.execute('SELECT * FROM opaska WHERE id=?', (band_id,)).fetchone()
        if band is None:
            return {'allowed': False, 'reason': 'unknown_wristband',
                    'message': f'Nieznana opaska {band_id}.'}

        cost = 0
        if band['typ'] == 'pass':
            if not band['wazna_do'] or datetime.fromisoformat(band['wazna_do']) <= datetime.now():
                return {'allowed': False, 'reason': 'expired',
                        'message': 'Karnet stracił ważność.'}
        else:
            cost = attr['koszt']
            if band['zetony'] < cost:
                return {'allowed': False, 'reason': 'not_enough_tokens',
                        'message': f"Brak żetonów: wymagane {cost}, dostępne {band['zetony']}."}
            db.execute('UPDATE opaska SET zetony=zetony-? WHERE id=?', (cost, band_id))

        db.execute('INSERT INTO wejscie(opaska_id,atrakcja_id,koszt_zetonow,czas) VALUES(?,?,?,?)',
                   (band_id, attr_id, cost, datetime.now().isoformat(timespec='seconds')))
        remaining = band['zetony'] - cost if band['typ'] == 'tokens' else None
        return {'allowed': True, 'reason': 'ok', 'message': 'Zezwolono na wejście.',
                'wristband_id': band_id, 'owner': band['wlasciciel'],
                'type': band['typ'], 'attraction': attr['nazwa'],
                'deducted': cost, 'remaining': remaining}
