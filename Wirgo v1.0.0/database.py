"""SQLite storage for Wirgo. Run: python database.py (creates demo database)."""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get('WIRGO_DB_PATH', str(BASE_DIR / 'wirgo.db')))

MENU = [
    ('m1', 'Zapiekanka tradycyjna', 1800, 'fa-bread-slice'),
    ('m2', 'Frytki duże z sosami', 1400, 'fa-bowl-rice'),
    ('m3', 'Hot Dog amerykański', 1500, 'fa-hotdog'),
    ('m4', 'Lody włoskie (dwusmak)', 1000, 'fa-ice-cream'),
    ('m5', 'Napój gazowany 0.5L', 800, 'fa-bottle-water'),
    ('m6', 'Kawa Espresso / Cappuccino', 1200, 'fa-mug-hot'),
]

ATTRACTIONS = [
    (1, 'Diabelski Młyn', 3, 'Działająca'),
    (2, "Kolejka Górska 'Ukiel'", 5, 'Działająca'),
    (3, 'Autodrom', 2, 'W trakcie naprawy'),
    (4, 'Dom Strachów', 4, 'Uszkodzona'),
    (5, 'Karuzela Wenecka', 2, 'Działająca'),
    (6, 'Spływ Rzeczny', 3, 'Działająca'),
    (7, 'Strzelnica Laserowa', 2, 'Działająca'),
    (8, 'Mini Coaster dla dzieci', 2, 'Działająca'),
    (9, 'Trampoliny', 1, 'Zamknięta'),
    (10, 'Wieża Swobodnego Spadku', 4, 'Działająca'),
]

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS opaska (
    id TEXT PRIMARY KEY,
    typ TEXT NOT NULL CHECK (typ IN ('tokens', 'pass')),
    zetony INTEGER NOT NULL DEFAULT 0 CHECK (zetony >= 0),
    wazna_do TEXT,
    wlasciciel TEXT NOT NULL DEFAULT 'Gość',
    utworzono TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS atrakcja (
    id INTEGER PRIMARY KEY,
    nazwa TEXT NOT NULL,
    koszt INTEGER NOT NULL CHECK (koszt >= 0),
    status TEXT NOT NULL CHECK (status IN ('Działająca', 'Uszkodzona', 'W trakcie naprawy', 'Zamknięta'))
);
CREATE TABLE IF NOT EXISTS produkt (
    id TEXT PRIMARY KEY,
    nazwa TEXT NOT NULL,
    cena_grosze INTEGER NOT NULL CHECK (cena_grosze >= 0),
    ikona TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS zamowienie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL DEFAULT 'Oczekujące',
    utworzono TEXT NOT NULL,
    suma_grosze INTEGER NOT NULL CHECK (suma_grosze >= 0)
);
CREATE TABLE IF NOT EXISTS pozycja_zamowienia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zamowienie_id INTEGER NOT NULL REFERENCES zamowienie(id),
    produkt_id TEXT NOT NULL REFERENCES produkt(id),
    ilosc INTEGER NOT NULL CHECK (ilosc > 0),
    cena_grosze INTEGER NOT NULL CHECK (cena_grosze >= 0)
);
CREATE TABLE IF NOT EXISTS wejscie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opaska_id TEXT NOT NULL REFERENCES opaska(id),
    atrakcja_id INTEGER NOT NULL REFERENCES atrakcja(id),
    koszt_zetonow INTEGER NOT NULL CHECK (koszt_zetonow >= 0),
    czas TEXT NOT NULL
);
"""


def _open_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


@contextmanager
def connect():
    connection = _open_connection()
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def transaction():
    connection = _open_connection()
    try:
        connection.execute('BEGIN IMMEDIATE')
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize():
    """Create schema and insert missing demo records; existing records stay intact."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.executescript(SCHEMA)
        db.executemany(
            'INSERT OR IGNORE INTO atrakcja(id, nazwa, koszt, status) VALUES (?, ?, ?, ?)',
            ATTRACTIONS,
        )
        db.executemany(
            'INSERT OR IGNORE INTO produkt(id, nazwa, cena_grosze, ikona) VALUES (?, ?, ?, ?)',
            MENU,
        )
        now = datetime.now().isoformat(timespec='seconds')
        demo = [
            ('PAS-001', 'tokens', 12, None, 'Jan Kowalski', now),
            ('PAS-002', 'tokens', 1, None, 'Anna Nowak', now),
            ('PAS-003', 'pass', 0, (datetime.now() + timedelta(days=1)).isoformat(timespec='seconds'), 'Piotr Zieliński', now),
        ]
        db.executemany(
            'INSERT OR IGNORE INTO opaska(id, typ, zetony, wazna_do, wlasciciel, utworzono) '
            'VALUES (?, ?, ?, ?, ?, ?)', demo,
        )
        db.commit()


if __name__ == '__main__':
    initialize()
    print(f'Baza gotowa: {DB_PATH}')
