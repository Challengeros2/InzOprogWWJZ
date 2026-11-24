@echo off
cd /d "%~dp0"
echo === Wirgo v1: uruchamianie ===
if not exist ".venv\Scripts\python.exe" (
    echo Tworzenie srodowiska Python...
    py -3 -m venv .venv
    if errorlevel 1 goto error
)
".venv\Scripts\python.exe" -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalowanie Flask - wymagany internet podczas pierwszego uruchomienia...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto error
)
echo Przygotowanie bazy (bez kasowania obecnych danych)...
".venv\Scripts\python.exe" database.py
if errorlevel 1 goto error
echo.
echo Otworz w przegladarce: http://127.0.0.1:5000
echo Zatrzymanie: Ctrl+C
echo.
".venv\Scripts\python.exe" -m flask --app app run
pause
exit /b 0
:error
echo.
echo BLAD: Nie udalo sie uruchomic Wirgo. Sprawdz Python 3 i polaczenie internetowe.
pause
exit /b 1
