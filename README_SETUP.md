# VoltWise setup

## Requirements

- Python 3.12 or newer
- MySQL 8.x for application and integration use
- A local virtual environment

## Project structure

- `frontend/` — Jinja templates and browser CSS/JavaScript assets
- `backend/` — Flask application, database models, migrations, and tests

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
```

Set the MySQL and secret values in `.env` before running the application.
Set `ELECTRICITY_RATE_PER_KWH` to the applicable tariff; it defaults to `0` until configured.

After updating an existing database, apply schema upgrades before starting the server:

```powershell
python -m backend.migrations.upgrade
```

```powershell
python run.py
```

Open `http://127.0.0.1:5000/`.

## Tests

```powershell
python -m pytest backend\tests -q
```
