# Instrukcje dla agentów – Wirgo

## 1. Projekt i zasady

- Projekt Wirgo wykorzystuje Python Flask, JavaScript i SQLite.
- Zachowuj istniejący podział MVC.
- Przed zmianami przeczytaj `README.md`, `docs/architektura-mvc.md` i `docs/przeplywy.md`.
- Zmieniaj tylko pliki potrzebne do wykonania zadania.
- Nie usuwaj istniejących funkcjonalności ani zapisanych danych.
- Nie zmieniaj struktury bazy danych ani adresów API bez uzgodnienia.
- Korzystaj wyłącznie z przykładowych danych.
- Nie wykonuj commitów ani nie wysyłaj zmian do GitHub bez zgody.

## 2. Podział MVC

- Model (`models/wirgo.py`) – sprawdzanie danych, reguły działania i zapis do bazy.
- Kontroler (`controllers/api.py`) – odbieranie żądań i przekazywanie ich do modelu.
- Widok (`templates/index.html`, `static/script.js`) – formularze, przyciski i wyświetlanie wyników.
- `database.py` – połączenie z bazą SQLite i jej inicjalizacja.
- `app.py` – uruchamianie aplikacji Flask.

## 3. Uruchamianie i testowanie

Polecenia należy wykonywać w głównym katalogu projektu.

Uruchomienie aplikacji w Windows:

```cmd
start-wirgo.bat
```

Testy automatyczne:

```cmd
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Sprawdzenie zmian w Git:

```cmd
git status --short
git diff
```

## 4. Sposób pracy

1. Najpierw sprawdź aktualny kod i dokumentację.
2. Przygotuj krótki plan oraz wskaż pliki do zmiany.
3. Poczekaj na zatwierdzenie planu.
4. Wprowadź tylko uzgodnione zmiany.
5. Uruchom odpowiednie testy i sprawdź wynik.
6. Podaj listę zmienionych plików i wyniki testów.

Jeżeli testów nie udało się wykonać, należy to zaznaczyć.
