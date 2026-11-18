"""P2: model danych poczatkowych i pomocnicze formatowanie danych z SQLite.

Pozostale reguly (F01-F06) beda przenoszone po jednej funkcji w P3.
"""
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
