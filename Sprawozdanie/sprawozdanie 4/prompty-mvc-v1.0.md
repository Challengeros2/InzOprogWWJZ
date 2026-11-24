# Wirgo – prompty MVC (Laboratorium 04)

**Czat AI:** ChatGPT (rozmowa w przeglądarce).  
**Etapy prac:** P4 17.11.2026 – 24.11.2026.

Poniżej zapisano uporządkowane, odtworzone wersje poleceń odpowiadających wykonanym etapom.

## 1. Porównanie promptów

**Prompt ogólny:**

> Przerób Wirgo na MVC.

**Prompt poprawiony:**

> Mamy działającą aplikację Wirgo w Python Flask, JavaScript i SQLite. Chcemy podzielić jej kod na model, widok i kontroler. Zachowaj wygląd strony, dotychczasowe adresy API, bazę danych i pięć funkcji MVP: F01, F02, F03, F05 oraz F06. Najpierw przygotuj plan zmian, bez pisania kodu. Wskaż pliki do zmiany i sposób sprawdzenia, czy nic nie zostało zepsute.

W poprawionym poleceniu określono technologie, zakres pracy i warunki poprawności. Dzięki temu nie trzeba było przebudowywać całej aplikacji.

**Doprecyzowanie promptu:** Przy tworzeniu szkieletu dopisano, aby poprawić importy i ścieżki między plikami oraz przygotować komplet zmienionych plików do podmiany. Pozwoliło to uniknąć ręcznego przenoszenia fragmentów kodu.

## 2. P1 – Plan MVC

**Prompt:**

> Projekt Wirgo działa lokalnie w Flask i korzysta z SQLite. Ma widoki kasjera, technika i bramki oraz funkcje F01, F02, F03, F05 i F06. Aktualne pliki to `app.py`, `database.py`, `templates/index.html` i `static/script.js`. Na podstawie dołączonego kodu zaproponuj prosty podział na MVC. Napisz, za co odpowiada każdy plik i w jakiej kolejności wprowadzać zmiany. Na razie nie generuj kodu.

**Wynik:** Przygotowano plan z kontrolerem `controllers/api.py`, modelem `models/wirgo.py` oraz pozostawieniem dotychczasowych widoków HTML i JavaScript. Ustalono kolejność: szkielet MVC, następnie F01, F02, F03, F05 i F06.

## 3. P2 – Przygotowanie szkieletu MVC

**Prompt:**

> Wykonaj pierwszy etap planu MVC w istniejącym Wirgo. Utwórz katalogi `controllers` i `models`. Przenieś obsługę strony głównej i `/api/state` do kontrolera, a pobieranie danych do modelu. Popraw importy i połączenia między plikami. Nie zmieniaj wyglądu strony ani działania pozostałych funkcji. Zwróć pełne zmienione pliki i napisz, jak uruchomić projekt oraz sprawdzić, czy dane się wyświetlają.

**Wynik:** Dodano pliki kontrolera i modelu oraz dostosowano `app.py`. Aplikacja uruchomiła się poprawnie, a widoki nadal wyświetlały dane. Po sprawdzeniu zapisano zmianę w Git.

## 4. P3 – Przeniesienie funkcji MVP

Dla każdej funkcji przygotowano osobne polecenie. W kolejnych krokach wykorzystywano aktualny kod po poprzedniej zmianie. Zachowano istniejące adresy API, wygląd strony i bazę danych.

### F01 – Wydawanie opasek i karnetów

**Prompt:**

> Przenieś obsługę F01 z `app.py` do `controllers/api.py` i `models/wirgo.py`. Kontroler ma odbierać dane z formularza, a model sprawdzać liczbę żetonów lub czas ważności karnetu i zapisywać nową opaskę w SQLite. Zachowaj istniejące API. Utworzenie opaski z 10 żetonami ma się udać, a liczba -5 ma zostać odrzucona. Podaj pliki do zmiany i sposób testowania.

**Wynik:** Przeniesiono tworzenie opasek do kontrolera i modelu. Poprawne dane były przyjmowane, a błędne odrzucane.

### F02 – Sprawdzanie salda i doładowanie

**Prompt:**

> Przenieś F02 do MVC. Kontroler ma przyjmować identyfikator opaski i liczbę żetonów, a model odczytywać saldo i aktualizować je w SQLite. Doładowanie o 5 żetonów powinno zwiększyć saldo. Ujemna wartość i nieznany identyfikator mają zwracać błąd. Zachowaj pozostałe funkcje i podaj sposób sprawdzenia.

**Wynik:** Odczyt salda i doładowanie przeniesiono do MVC. Poprawne doładowania były zapisywane, a błędne dane odrzucane.

### F03 – Zamówienia gastronomiczne

**Prompt:**

> Przenieś F03 do kontrolera i modelu. Kasjer wybiera produkty i ich ilość, a model sprawdza dane, oblicza cenę i zapisuje zamówienie w SQLite. Zamówienie z poprawnym produktem powinno zostać dodane, a nieznany produkt lub błędna ilość powinny zostać odrzucone. Nie zmieniaj interfejsu ani wcześniejszych funkcji. Podaj zmienione pliki i testy.

**Wynik:** Zapis zamówień przeniesiono do modelu. Zamówienia działały w dotychczasowym interfejsie.

### F05 – Stan atrakcji

**Prompt:**

> Przenieś F05 do MVC. Kontroler ma przyjmować wybraną atrakcję i jej nowy status, a model sprawdzać, czy atrakcja i status istnieją, oraz zapisywać zmianę w SQLite. Poprawny status ma się zapisać, a nieznany, np. `XYZ`, ma zostać odrzucony. Zachowaj działanie bramki i pozostałych funkcji. Podaj sposób sprawdzenia.

**Wynik:** Aktualizacja statusu atrakcji została przeniesiona do modelu. Zmiany były widoczne także w panelu bramki.

### F06 – Kontrola wejścia

**Prompt:**

> Przenieś F06 do MVC. Pracownik wpisuje identyfikator opaski i wybiera atrakcję. Model ma sprawdzić istnienie opaski, stan atrakcji, saldo żetonów lub ważność karnetu. Przy poprawnym wejściu odejmij wymagane żetony i zapisz wynik w SQLite. Przy braku żetonów, nieważnym karnecie lub zamkniętej atrakcji odmów wejścia z komunikatem. Nie zmieniaj pozostałych funkcji. Podaj pliki i kroki testowe.

**Wynik:** Sprawdzanie wejścia przeniesiono do modelu. Po zakończeniu F05 i F06 uruchomiono testy automatyczne: **8 z 8 zakończyło się poprawnie**. Sprawdzono również główne funkcje w przeglądarce.

## 5. P4 – Końcowy przegląd

**Prompt:**

> Sprawdź końcowy kod Wirgo i porównaj go z planem MVC oraz funkcjami MVP z laboratorium 02. Oceń, czy kontroler obsługuje żądania, model sprawdza reguły i korzysta z SQLite, a widok pokazuje wyniki. Zwróć uwagę na zachowanie danych po ponownym uruchomieniu. Jeśli znajdziesz błąd, zaproponuj najmniejszą poprawkę i sposób jej sprawdzenia. Jeśli wszystko jest zgodne, nie zmieniaj kodu bez potrzeby.

**Wynik:** Sprawdzono podział plików oraz podstawowe operacje modelu. Nie stwierdzono potrzeby dalszych zmian w pięciu funkcjach MVP. Zaktualizowano opis architektury. Testy automatyczne i ręczne wykonane wcześniej po zmianach MVC zakończyły się poprawnie.

## 6. Wnioski

Podzielenie pracy na mniejsze prompty ułatwiło przeniesienie kodu do MVC. Zachowano poprzedni wygląd aplikacji i działanie pięciu funkcji MVP.
