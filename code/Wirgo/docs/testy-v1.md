# Wirgo v1 – scenariusze sprawdzenia (Laboratorium 03)

Wyników działania aplikacji na komputerze użytkownika **nie wpisano z góry**. Oznaczenie `niewykonany` oznacza konieczność ręcznego sprawdzenia.

## Testy ręczne w przeglądarce

| Nr | Funkcja | Kroki / dane wejściowe | Oczekiwany rezultat | Wynik |
|---|---|---|---|---|
| T01 | Start/Widoki | Uruchom Flask, wejdź na `127.0.0.1:5000`, klikaj Kasjer, Technik, Bramka | Widoki się pokazują, brak błędów ładowania | niewykonany |
| T02 | F01 | Kasjer: opaska żetonowa, 10 żetonów, Utwórz | Nowe ID opaski, opaska dostępna na bramce | niewykonany |
| T03 | F01 | Kasjer: karnet 3 dni | Nowa opaska z datą ważności +3 dni | niewykonany |
| T04 | F01 | Kasjer: 0 lub -5 żetonów | Komunikat błędu, brak nowej opaski | niewykonany |
| T05 | F02 | Kasjer: `PAS-001`, przycisk Sprawdź | Pokazuje saldo opaski | niewykonany |
| T06 | F02 | Kasjer: `PAS-001`, doładowanie 5 | Saldo rośnie o 5 | niewykonany |
| T07 | F02 | Kasjer: `PAS-001`, doładowanie -3 | Błąd, saldo bez zmian | niewykonany |
| T08 | F03 | Dodaj 2 zapiekanki i 1 napój, Finalizuj | Zamówienie zapisane; suma 44 PLN; widoczne w kuchni | niewykonany |
| T09 | F03 | Spróbuj finalizować pusty koszyk | Przycisk pozostaje nieaktywny | niewykonany |
| T10 | F05 | Technik: ustaw Diabelski Młyn na Uszkodzona | Widok pokazuje nowy status | niewykonany |
| T11 | F06 | Bramka: `PAS-001`, działający Diabelski Młyn | Wejście dozwolone, pobiera 3 żetony | niewykonany |
| T12 | F06 | Bramka: `PAS-002`, działający Diabelski Młyn | Odmowa: za mało żetonów; saldo bez zmian | niewykonany |
| T13 | F06 | Bramka: `PAS-001`, uszkodzony Diabelski Młyn | Odmowa wejścia, nie pobiera żetonów | niewykonany |
| T14 | F06 | Bramka: `PAS-999` | Odmowa dla nieznanej opaski | niewykonany |
| T15 | Trwałość | Utwórz/doładuj opaskę, zrób zamówienie, zmień status; zatrzymaj i ponownie uruchom Flask | Dane nadal istnieją, nie wracają do demo wartości | niewykonany |
| T16 | Dwa komputery | Druga osoba pobiera repozytorium, instaluje zależności, inicjalizuje bazę i uruchamia aplikację | Wirgo działa lokalnie również u drugiej osoby | niewykonany |

**Uwaga:** T11 wykonaj po przywróceniu statusu `Działająca` w panelu technika. T12 zakłada oryginalne demo saldo `PAS-002 = 1`.

## Testy automatyczne

Po instalacji Flask wykonaj:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Testy znajdują się w `tests/test_app.py`. Sprawdzają widoki, poprawne i błędne operacje na opaskach, zamówienia, statusy atrakcji, weryfikację wejścia, wygaśnięcie karnetu, zapis danych w SQLite i brak utraty danych po ponownej inicjalizacji.

**Wynik:** do uzupełnienia po uruchomieniu na komputerze z zainstalowanym Flask. W środowisku przygotowania pakietu sprawdzono składnię Python i JavaScript oraz inicjalizację SQLite, ale nie udało się zainstalować Flask z uwagi na brak dostępu do serwera pakietów. Nie należy oznaczać powyższych testów jako `działa`, dopóki nie zostaną naprawdę uruchomione.

## Rejestr błędów

| Data | Scenariusz | Oczekiwane / faktyczne zachowanie | Poprawka | Test ponowny |
|---|---|---|---|---|
| [wpisać] | [wpisać] | [wpisać] | [wpisać] | [wpisać] |
