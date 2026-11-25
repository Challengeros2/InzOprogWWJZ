# Wirgo – Przepływy funkcji

## 1. F02 – Sprawdzanie salda i doładowywanie opaski

**Użytkownik:** Kasjer.

**Dane wejściowe:** identyfikator opaski oraz liczba żetonów do dodania.

**Przebieg działania:**

1. Kasjer podaje identyfikator opaski i liczbę żetonów.
2. Widok wysyła żądanie `POST /api/wristbands/<band_id>/recharge` do kontrolera w `controllers/api.py`.
3. Kontroler przekazuje dane do funkcji `top_up_wristband()` w `models/wirgo.py`.
4. Model sprawdza, czy opaska istnieje, czy jest żetonowa i czy liczba dodawanych żetonów jest poprawna.
5. Przy poprawnych danych model zwiększa saldo w bazie SQLite. Przy błędnych danych saldo pozostaje bez zmian.
6. Widok wyświetla aktualne saldo albo komunikat błędu.

Saldo można również sprawdzić przez `GET /api/wristbands/<band_id>`, który korzysta z funkcji `read_wristband()`.

## 2. Sprawdzenie działania

Do prób wykorzystano opaskę `PAS-001`, której początkowe saldo wynosiło 12 żetonów. Najpierw wykonano poprawne doładowanie, a następnie próbę z błędną wartością.

| Próba | Dane wejściowe | Wynik oczekiwany | Wynik faktyczny | Status |
|---|---|---|---|---|
| Poprawna | `PAS-001`, 5 żetonów | Saldo wzrasta z 12 do 17 i zostaje zapisane. | Test potwierdził saldo 17 w bazie SQLite. | Poprawny |
| Błędna | `PAS-001`, -1 żeton | Doładowanie zostaje odrzucone, a saldo nie zmienia się. | Zwrócono błąd 400. Saldo pozostało równe 17. | Poprawny |

Powyższe wyniki pochodzą z istniejącego testu `test_f02_balance_topup_validation_and_persistence`. W poprzednim uruchomieniu cały zestaw ośmiu testów zakończył się poprawnie. Wyniki należy ponownie sprawdzić po wprowadzeniu kolejnych zmian.

## 3. Wykorzystanie AI

Do przeglądu funkcji F02 przygotowano następujące polecenie:

> Przeczytaj `AGENTS.md`, `docs/architektura-mvc.md` i kod funkcji F02. Sprawdź, czy kontroler obsługuje żądanie, a model weryfikuje dane i zapisuje saldo. Zaproponuj jeden dodatkowy test poprawnego i błędnego doładowania. Na razie nie zmieniaj kodu.

Wynik przeglądu agenta zostanie dopisany po wykonaniu polecenia.

## 4. Ocena i decyzja

Obecna obsługa F02 jest zgodna z przyjętym podziałem MVC. Kontroler przyjmuje żądanie, natomiast model sprawdza dane i aktualizuje saldo w SQLite.

Proponowane jest pozostawienie działającej funkcji bez zmian i dodanie testu sprawdzającego reguły modelu. Ostateczną decyzję i wynik nowego testu należy zapisać po ich wykonaniu.
