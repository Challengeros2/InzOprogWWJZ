# Wirgo – Technologie (Laboratorium 03)

## Wybór i uzasadnienie (7 zdań)

Do przygotowania wersji v1 projektu Wirgo wybraliśmy HTML, CSS i JavaScript do wyświetlania interfejsu i obsługi przycisków. Zachowujemy istniejący wygląd prototypu, który wykorzystuje Tailwind CSS ładowany z CDN. Po stronie serwera korzystamy z Pythona i biblioteki Flask, ponieważ pozwalają one tworzyć proste adresy API bez rozbudowanej konfiguracji. Serwer sprawdza poprawność danych, decyduje o wpuszczeniu gościa na atrakcję i zapisuje zmiany. Dane przechowujemy w SQLite, czyli lokalnej bazie danych w jednym pliku, obsługiwanej przez wbudowany moduł `sqlite3`. Dzięki temu opaski, zamówienia oraz stany atrakcji nie znikają po odświeżeniu strony ani restarcie aplikacji. Do pracy zespołowej wykorzystujemy edytor kodu, Git i GitHub, aby zapisywać kolejne etapy projektu.

## Użyte narzędzia i ich role

| Obszar | Wybór | Rola |
|---|---|---|
| Widoki | HTML5, CSS3, JavaScript (ES6+) | Formularze, zakładki i komunikaty |
| Styl | Tailwind CSS przez CDN, Font Awesome przez CDN | Wygląd i ikony istniejącego prototypu |
| Serwer | Python 3.10+ i Flask 3.x | Udostępnianie strony i walidacja żądań |
| Dane | SQLite / moduł `sqlite3` z Pythona | Trwały lokalny zapis, PK/FK |
| Praca zespołowa | Git, GitHub, dowolny edytor | Wersjonowanie i współpraca |
| Czat AI | ChatGPT (rozmowa w przeglądarce) | Planowanie i wsparcie generowania kodu |

Wymagane wersje środowiska: Python 3.10 lub nowszy, Flask w zakresie `>=3.0,<4.0`. Dokładne wersje z komputerów obu członków zespołu należy uzupełnić po wykonaniu `python --version`, `python -m flask --version` i `git --version`.

## Rozważone warianty

1. **Sama strona HTML/JS z localStorage.** Najmniej plików, ale nie odpowiada dobrze wymaganiu oddzielnego serwera i relacyjnej bazy danych.
2. **HTML/JS + Flask + SQLite.** Wymaga uruchomienia Pythona, ale spełnia wymagania Lab 03 i pozwala zachować wygląd Wirgo.

**Decyzja:** wariant drugi. Nie korzystamy z usług płatnych, zewnętrznego hostingu, kluczy API ani prawdziwych czytników RFID.
