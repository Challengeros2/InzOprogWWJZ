# Wirgo – Architektura MVC

## 1. Cel i podział aplikacji

Aplikacja Wirgo wykorzystuje prosty podział MVC, który oddziela obsługę danych, interfejs użytkownika i obsługę żądań. System korzysta z Flask oraz bazy SQLite i realizuje pięć podstawowych funkcjonalności.

| Element | Plik | Zadanie |
|---|---|---|
| Model | [models/wirgo.py](../models/wirgo.py) | Sprawdzanie danych, reguły działania oraz odczyt i zapis w SQLite. |
| Widok | [templates/index.html](../templates/index.html) | Wygląd strony i formularze. |
| Widok | [static/script.js](../static/script.js) | Obsługa przycisków, wysyłanie żądań i pokazywanie komunikatów. |
| Kontroler | [controllers/api.py](../controllers/api.py) | Odbieranie żądań, wywoływanie modelu i zwracanie wyników. |
| Uruchomienie | [app.py](../app.py) | Uruchamianie aplikacji Flask i podłączenie kontrolera. |
| Baza danych | [database.py](../database.py) | Połączenie z SQLite, tworzenie tabel i dane przykładowe. |

Dodatkowa obsługa statusów zamówień kuchni pozostała w `app.py`. Jest to funkcja demonstracyjna spoza wybranego MVP.

## 2. Funkcjonalności MVP

| ID | Funkcjonalność | Widok | Funkcja modelu |
|---|---|---|---|
| F01 | Wydawanie opasek i karnetów | Kasjer | `issue_wristband()` |
| F02 | Sprawdzanie salda i doładowania | Kasjer | `read_wristband()`, `top_up_wristband()` |
| F03 | Tworzenie zamówień gastronomicznych | Kasjer | `create_food_order()` |
| F05 | Zmiana stanu atrakcji | Technik | `change_attraction_status()` |
| F06 | Kontrola wejścia na atrakcje | Bramka | `verify_attraction_entry()` |

Wszystkie wymienione funkcje obsługuje kontroler `controllers/api.py`, który przekazuje dane do odpowiednich funkcji w modelu `models/wirgo.py`.

## 3. Zależności między modułami

Przeglądarka wysyła żądanie do kontrolera. Kontroler wywołuje model, który sprawdza reguły i korzysta z bazy SQLite. Wynik wraca do przeglądarki, gdzie zostaje wyświetlony użytkownikowi.

`Widok → Kontroler → Model → SQLite → Model → Kontroler → Widok`

Opisany podział działa dla wszystkich pięciu funkcji MVP.

## 4. Przepływ F02 – doładowanie opaski

1. Kasjer wpisuje identyfikator opaski i liczbę żetonów w formularzu.
2. JavaScript wysyła żądanie `POST /api/wristbands/<band_id>/recharge`.
3. Kontroler wywołuje w modelu funkcję `top_up_wristband()`.
4. Model sprawdza, czy opaska istnieje, czy jest żetonowa i czy liczba żetonów jest dodatnią liczbą całkowitą.
5. Przy poprawnych danych saldo w tabeli `opaska` zostaje zwiększone. Przy błędnych danych saldo się nie zmienia.
6. Wynik wraca do widoku, który wyświetla potwierdzenie lub komunikat błędu.

Stan opaski można odczytać przez `GET /api/wristbands/<band_id>`. Próby poprawnego i błędnego doładowania opisano w [przeplywy.md](przeplywy.md).

## 5. Przykład działania F06 – kontrola wejścia

1. Pracownik wybiera atrakcję i wpisuje identyfikator opaski w panelu bramki.
2. Kontroler odbiera żądanie i wywołuje `verify_attraction_entry()`.
3. Model sprawdza w SQLite status atrakcji, ważność opaski i dostępne żetony.
4. Jeśli wejście jest dozwolone, model zapisuje wejście i w razie potrzeby odejmuje żetony.
5. Widok wyświetla zgodę albo przyczynę odmowy wejścia.

## 6. Podsumowanie

Wszystkie pięć funkcji MVP korzysta z podziału MVC. Zachowano istniejący interfejs i adresy API. Aplikacja przeszła osiem testów automatycznych, a jej główne funkcje sprawdzono również w przeglądarce.
