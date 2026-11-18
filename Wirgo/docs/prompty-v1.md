# Wirgo – Prompty AI i decyzje (Laboratorium 03)

**Narzędzie:** ChatGPT (czat w przeglądarce). **Projekt:** Wirgo v1.

Poniżej zapisano polecenia przygotowane do kolejnych etapów Lab 03 oraz przyjęte decyzje projektowe. Nie są to automatycznie wygenerowane logi wszystkich wiadomości z rozmowy. Każdy członek zespołu powinien dopisać własny użyty czat, faktyczne poprawki i commity.

## P0 – Rola widoku, serwera i bazy

> Wyjaśnij na przykładzie rezerwacji sali, co robi widok, serwer i baza danych.

**Wniosek:** widok pokazuje formularz, serwer sprawdza reguły i obsługuje żądanie, baza danych trwale przechowuje rekordy. W Wirgo widok wydaje opaskę, serwer waliduje jej typ i saldo, a baza zapisuje opaskę.

## P1 – Dobór technologii

> Pracujemy we dwoje nad Wirgo, prostym systemem obsługi parku rozrywki. Widoki v1: W01 kasjer, W03 technik, W04 bramka. Funkcje MVP: F01 sprzedaż opasek, F02 doładowanie, F03 zamówienie gastronomiczne, F05 status atrakcji, F06 symulacja wejścia. Dane: Opaska, Atrakcja, Produkt, Zamówienie, PozycjaZamówienia i Wejście. Mamy działający prototyp HTML/JS. Porównaj dwa bezpłatne rozwiązania lokalne, z których jedno umożliwi SQLite, i wybierz prostsze spełniające wymagania.

**Decyzja:** Flask + SQLite, zachowanie obecnego interfejsu HTML/JS. Prototyp jest w `archive/original.html`.

## P2 – Szkielet

> Na podstawie załączonego pojedynczego pliku HTML Wirgo przenieś logikę JavaScript do `static/script.js`, interfejs do `templates/index.html` i utwórz `app.py` z Flask. Nie zmieniaj układu widoków ani nie dodawaj nowych funkcji. Podaj instrukcję uruchomienia oraz strukturę plików.

**Zrealizowane w kodzie:** szablon strony, osobny skrypt, serwer Flask i `requirements.txt`.

## P3 – Widoki

> Zachowaj układ kasjera, technika i bramki z prototypu. Upewnij się, że są podpisane pola, nawigacja, komunikaty błędów i sukcesu. Nie implementuj logowania i fizycznego RFID. Przedstaw sposób ręcznego sprawdzenia wszystkich trzech ekranów.

**Decyzja:** W01, W03 i W04 są wymagane w v1. Ekrany kuchni i menedżera pozostają pomocniczym demonstracyjnym prototypem v2.

## P4 – SQLite

> Dodaj do Wirgo lokalną bazę SQLite z tabelami `opaska`, `atrakcja`, `produkt`, `zamowienie`, `pozycja_zamowienia`, `wejscie`. Dodaj PK/FK, zapytania parametryzowane, `PRAGMA foreign_keys=ON`, fikcyjne dane i polecenie oddzielnej inicjalizacji. Ponowna inicjalizacja nie może nadpisywać już zapisanych danych.

**Zrealizowane w kodzie:** `database.py`; plik `wirgo.db` powstaje lokalnie po `python database.py`.

## P5 – Funkcje MVP

> Podłącz kolejno F01 (wydanie opaski), F02 (sprawdzenie i doładowanie), F03 (zamówienie), F05 (zmiana stanu atrakcji), F06 (weryfikacja wejścia) do Flask i SQLite. Każdą operację waliduj po stronie serwera. Przy błędzie zwracaj czytelny komunikat. Nie pozwalaj na ujemne doładowania ani wejście na niedostępną atrakcję.

**Zrealizowane w kodzie:** adresy API `/api/wristbands`, `/api/orders`, `/api/attractions/.../status` i `/api/entry`. Kod frontendowy korzysta z `fetch`.

## P6 – Weryfikacja błędu (szablon do prawdziwego zgłoszenia)

> Uruchomiłem program poleceniem: [polecenie]. Kroki odtworzenia: [kroki]. Oczekiwałem: [wynik]. Otrzymałem: [wynik]. Komunikat: [pełna treść]. Aktualne pliki: [kod]. Popraw błąd i powiedz, jak sprawdzić również wcześniejsze funkcje.

**Własne poprawki projektowe uwzględnione w kodzie:** blokowanie ujemnych doładowań, rozróżnianie karnetów 1/3/7 dni, walidacja daty ważności, wyświetlanie wszystkich czterech statusów atrakcji, zabezpieczenie zapisu żetonów w jednej transakcji SQLite.

## P7 – Testy

> Porównaj kod Wirgo z funkcjami F01, F02, F03, F05 i F06. Zapisz przypadki pozytywne, negatywne oraz test zachowania danych po ponownym uruchomieniu. Rozdziel testy automatyczne od manualnych i nie wpisuj fikcyjnych wyników.

**Rezultat:** `tests/test_app.py` oraz `docs/testy-v1.md`.

## Do uzupełnienia przez zespół

| Pole | Wpis |
|---|---|
| Czat wybrany przez osobę 1 | ChatGPT / potwierdzić użyty wariant |
| Czat wybrany przez osobę 2 | [wpisać] |
| Własne poprawki osoby 1 | [wpisać po sprawdzeniu] |
| Własne poprawki osoby 2 | [wpisać po sprawdzeniu] |
| Commity w GitHub | [dodać identyfikatory] |
| Decyzje i stan zadań w LaboChat | [dodać link] |
