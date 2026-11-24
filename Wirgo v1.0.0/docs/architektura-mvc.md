# Wirgo – plan i szkielet MVC (Laboratorium 04)

## P1 – Plan

Zachowujemy dotychczasowy interfejs oraz bazę SQLite. Dzielimy istniejący kod na trzy części:

- **Model:** `models/wirgo.py` – pobieranie i przygotowanie danych z SQLite. Obsługa kolejnych funkcji zostanie przeniesiona w P3.
- **Widok:** `templates/index.html` i `static/script.js` – formularze i wyświetlanie informacji.
- **Kontroler:** `controllers/api.py` – przyjmuje żądania HTTP i wywołuje model.

`app.py` uruchamia Flask i rejestruje kontroler. `database.py` zapewnia połączenie z SQLite i inicjalizację danych.

## P2 – Pierwszy działający podział

Przeniesiono obsługę strony głównej (`/`) i pobierania danych (`/api/state`) do `controllers/api.py`. Pobieranie danych z bazy umieszczono w `models/wirgo.py`. Formularze i wyświetlanie wyników pozostały bez zmian.

Przepływ: przeglądarka otwiera stronę → kontroler zwraca HTML → JavaScript pobiera `/api/state` → kontroler wywołuje model → model odczytuje SQLite → przeglądarka wyświetla dane.

Pozostałe funkcje F01, F02, F03, F05, F06 nadal działają w dotychczasowym `app.py`. Ich przenoszenie przewidziano osobno w P3, aby nie zmieniać wszystkiego naraz.

## Kolejność dalszych prac

1. P3 – F01: tworzenie opasek.
2. P3 – F02: sprawdzanie i doładowanie opaski.
3. P3 – F03: zapisywanie zamówień.
4. P3 – F05: aktualizacja stanu atrakcji.
5. P3 – F06: weryfikacja wejścia.
6. P4 – ponowne testowanie i poprawki, jeśli będą potrzebne.

To jest dokumentacja aktualnego etapu P2, nie opis zakończonej wersji 1.0.
