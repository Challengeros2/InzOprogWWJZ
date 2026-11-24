# Wirgo

A simple browser-based amusement park management system, built as a university project.

**Stack:** HTML, JavaScript, Tailwind CSS (CDN), Python / Flask, SQLite.

## Run locally

Requires **Python 3.10+**. On Windows, you can simply double-click **`start-wirgo.bat`** (first run installs Flask and prepares the demo database). Then visit `http://127.0.0.1:5000`. Alternatively, use the terminal commands below. Open a terminal in the project folder.

**Windows (PowerShell):**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe database.py
.\.venv\Scripts\python.exe -m flask --app app run
```

**Linux / macOS:**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python database.py
.venv/bin/python -m flask --app app run
```

Open **http://127.0.0.1:5000** in your browser. Stop the server with **Ctrl+C**.

The SQLite database is created locally as `wirgo.db` (not committed to Git). Running `database.py` again **does not erase** existing data. To return to the initial demo state, stop Flask, delete `wirgo.db`, then run `database.py` again.

The app simulates wristbands using typed IDs; **no real RFID reader, payment system or login** is provided. Role tabs are demonstrations, not access controls. The manager schedule is still an in-browser v2 prototype; v1 wristbands, orders, attraction statuses and entries are stored in SQLite. Styling/icons are loaded from public CDNs, so internet access is helpful for the intended appearance.

## Tests

After installing requirements:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Linux/macOS: replace the Python executable with `.venv/bin/python`.

## Documentation

- [Roadmap v1](docs/roadmap-v1.md)
- [Technology choices](docs/technologie.md)
- [AI prompts and decisions](docs/prompty-v1.md)
- [v1 test scenarios/results](docs/testy-v1.md)

The initial single-file prototype is kept in `archive/original.html`.

## Team

- [Member 1 — GitHub username / index number]
- [Member 2 — GitHub username / index number]

LaboChat project: [add link]
