# Wirgo – System Zarządzania Parkiem Rozrywki

Wirgo to prosta aplikacja internetowa służąca do obsługi parku rozrywki. Umożliwia sprzedaż biletów, zarządzanie wirtualnymi opaskami, tworzenie zamówień gastronomicznych, zmianę stanu atrakcji oraz kontrolowanie wejść.

Projekt wykorzystuje HTML, JavaScript, Python Flask oraz bazę danych SQLite.

## Uruchomienie

Do uruchomienia wymagany jest Python 3.

Na Windows można uruchomić plik `start-wirgo.bat`, który przygotowuje środowisko i uruchamia aplikację.

Można również użyć terminala:

```cmd
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe database.py
.venv\Scripts\python.exe -m flask --app app run
```

Następnie należy otworzyć w przeglądarce adres:

http://127.0.0.1:5000

## Testowanie

Testy automatyczne można uruchomić poleceniem:

```cmd
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Dokumentacja

- [Architektura MVC](docs/architektura-mvc.md)
- [Przepływy funkcji](docs/przeplywy.md)
- [Decyzja dotycząca doładowania opaski](docs/decyzje/001-doladowanie-opaski.md)
- [Road Map v1](docs/roadmap-v1.md)

## Informacje dodatkowe

Aplikacja działa lokalnie i korzysta z przykładowych danych. Opaski RFID są symulowane za pomocą identyfikatorów, bez używania fizycznych czytników. Dane są zapisywane w lokalnej bazie SQLite.