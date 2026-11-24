# Wirgo – testy MVP 1.0 (Laboratorium 04)

## 1. Uruchomienie

Aplikacja została uruchomiona lokalnie w Windows z użyciem `start-wirgo.bat`. Po zmianach MVC potwierdzono poprawne działanie interfejsu w przeglądarce.

Testy automatyczne uruchomiono poleceniem:

```cmd
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**Wynik po P3: 8 testów, 8 zaliczonych, OK.**

## 2. Testy automatyczne

| Sprawdzany element | Przypadek poprawny i błędny | Wynik |
|---|---|---|
| F01 – opaski i karnety | Poprawna liczba żetonów lub karnet; odrzucenie niedozwolonej wartości | działa |
| F02 – saldo i doładowanie | Zwiększenie salda; odrzucenie ujemnej liczby, nieznanej opaski i doładowania karnetu | działa |
| F03 – zamówienia | Zapis pozycji i ceny; odrzucenie nieznanego produktu | działa |
| F05 – atrakcje | Zapis nowego statusu; odrzucenie nieznanego statusu | działa |
| F06 – wejście żetonowe | Poprawne wejście i pobranie żetonów; odmowa przy braku salda, nieznanej opasce i zamkniętej atrakcji | działa |
| F06 – karnet | Aktywny karnet; odmowa po wygaśnięciu | działa |
| Widoki i dane demo | Strona główna, 10 atrakcji, 3 opaski, 6 produktów | działa |
| Kuchnia (demonstracja) | Zmiana statusu zamówienia | działa |

Testy sprawdzają również zapis w SQLite i zachowanie zmienionych danych po ponownym uruchomieniu inicjalizacji bazy.

## 3. Testy ręczne

| Scenariusz | Wynik |
|---|---|
| Otwarcie aplikacji i przechodzenie między widokami | działa |
| Wydanie opaski, doładowanie i zamówienie przez panel kasjera | działa |
| Zmiana stanu atrakcji w panelu technika | działa |
| Próba wejścia przez bramkę | działa |

## 4. Podsumowanie

Wszystkie osiem testów automatycznych przeszło poprawnie. Potwierdzono również działanie głównych funkcji w przeglądarce po zmianach MVC.
