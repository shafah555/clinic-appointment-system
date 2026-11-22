# CarePoint Clinic Appointment Management System (CAMS)

**Academic SDLC assignment demonstration — not a real clinic system.**

A small Flask web application demonstrating doctor search, appointment requests, appointment status management, demo billing, notifications, design patterns, tests, GitHub Actions, and a basic API.

## Features

1. Doctor directory and specialization search
2. Appointment booking with duplicate doctor/time-slot prevention
3. Appointment status updates
4. Demo invoice generation
5. Notification centre
6. JSON API for doctors and appointments

## Technology

Python 3.12, Flask, Flask-SQLAlchemy, SQLite locally / PostgreSQL on Render with Neon, Pytest, Selenium example, GitHub Actions.

## Run locally (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -c "from app import app, db, Doctor; app.app_context().push(); db.create_all(); db.session.add_all([Doctor(name='Dr. Ayesha Rahman', specialization='Cardiology', fee=800), Doctor(name='Dr. Tanvir Hasan', specialization='Dermatology', fee=600), Doctor(name='Dr. Nusrat Jahan', specialization='Medicine', fee=500)]); db.session.commit()"
python app.py
```

Open http://127.0.0.1:5000

If you use macOS/Linux, activate the environment with `source .venv/bin/activate`.

## Run tests

```bash
pytest --cov=app --cov-report=term-missing
```

Optional Selenium test: start the web application in one terminal, install Chrome and a compatible ChromeDriver, then in another terminal run:

```bash
RUN_SELENIUM=1 pytest tests/test_selenium_example.py
```

## Design patterns in this project

- **Factory Method:** `patterns/user_factory.py` creates role-specific user objects.
- **Facade:** `patterns/appointment_facade.py` offers a simplified booking workflow.
- **Observer:** `patterns/observer.py` broadcasts appointment notifications to observers.

## API

- `GET /api/doctors`
- `GET /api/appointments`

OpenAPI description: `openapi.yaml`. It can be viewed using https://editor.swagger.io/ by importing the file.

## Deploy to GitHub

Create an empty GitHub repository, then run:

```bash
git init
git add .
git commit -m "Initial CarePoint clinic application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your own repository URL.

## Deploy to Render + Neon

1. Create a PostgreSQL database in Neon.
2. Copy its pooled or direct connection string and keep it private.
3. In Render, create a **Web Service** connected to your GitHub repository.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variable `DATABASE_URL` with the Neon connection string.
7. Add `SECRET_KEY` with a long random value.
8. Deploy.
9. Initialize the database from Render Shell:

```bash
flask --app app init-db
```

The `init-db` command creates tables and sample doctors. Do not publish database credentials in GitHub.

## Deploy to Vercel

This repository includes `vercel.json` and `api/index.py` as a basic Python serverless entry point. Import the GitHub repository into Vercel and add `DATABASE_URL` and `SECRET_KEY` environment variables. Serverless deployments may need database connection pooling and may have platform/runtime constraints; for this simple assignment, Render + Neon is the recommended deployment route. If Vercel's build fails, use the Render deployment as the primary live demo and document Vercel as an attempted platform rather than claiming success.


## Project report

See `docs/REPORT_GUIDE.md` for the suggested report structure and screenshot checklist.
