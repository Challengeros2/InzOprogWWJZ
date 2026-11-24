# Wirgo – architektura MVC (Laboratorium 04)

## 1. Cel

W laboratorium 04 uporządkowano kod Wirgo według prostego podziału MVC. Wykorzystano aplikację z laboratorium 03. Zachowano jej wygląd, bazę SQLite i pięć funkcji MVP.

## 2. Podział plików

| Plik | Zadanie |
|---|---|
| `models/wirgo.py` | Model – sprawdzanie danych, reguły działania oraz odczyt i zapis w bazie. |
| `templates/index.html` | Widok – wygląd strony i formularze. |
| `static/script.js` | Widok – obsługa przycisków, wysyłanie danych i pokazywanie komunikatów. |
| `controllers/api.py` | Kontroler – odbieranie żądań, wywoływanie modelu i zwracanie wyników. |
| `app.py` | Uruchamianie aplikacji Flask i podłączenie kontrolera. |
| `database.py` | Połączenie z SQLite, tworzenie tabel i dane przykładowe. |

Dodatkowa obsługa statusów zamówień kuchni pozostała w `app.py`. Jest to funkcja demonstracyjna spoza wybranego MVP.

## 3. Funkcjonalności MVP

| ID | Funkcjonalność | Widok | Funkcja modelu |
|---|---|---|---|
| F01 | Wydawanie opasek i karnetów | Kasjer | `issue_wristband()` |
| F02 | Sprawdzanie salda i doładowania | Kasjer | `read_wristband()`, `top_up_wristband()` |
| F03 | Tworzenie zamówień gastronomicznych | Kasjer | `create_food_order()` |
| F05 | Zmiana stanu atrakcji | Technik | `change_attraction_status()` |
| F06 | Kontrola wejścia na atrakcje | Bramka | `verify_attraction_entry()` |

Wszystkie wymienione funkcje są obsługiwane przez `controllers/api.py`, który przekazuje dane do odpowiednich funkcji w `models/wirgo.py`.

## 4. Przykład działania – F06

1. W panelu bramki wpisywany jest identyfikator opaski i wybierana atrakcja.
2. JavaScript przesyła te dane do kontrolera.
3. Kontroler wywołuje funkcję `verify_attraction_entry()` w modelu.
4. Model sprawdza dane w SQLite. Jeśli wejście jest dozwolone, zapisuje je i w razie potrzeby odejmuje żetony.
5. Wynik wraca do przeglądarki, gdzie wyświetlana jest zgoda lub odmowa wejścia.

## 5. Podsumowanie

Najpierw przygotowano szkielet MVC i pobieranie danych (P2). Następnie przeniesiono kolejno F01, F02, F03, F05 i F06 (P3). Nie zmieniono wyglądu aplikacji ani dotychczasowych adresów API. Po zmianach wszystkie osiem testów automatycznych zakończyło się poprawnie. Sprawdzono też ręcznie działanie głównych funkcji w przeglądarce.
