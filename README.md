# Risk-Whisperers (RiskSys) — Web-Based Asset Risk Management System

## Project Overview

Risk-Whisperers (a.k.a. RiskSys) is a web-based Asset Risk Management System developed as an academic final-year BSc Information Technology (Software Engineering) project. The repository contains a Django-based application together with static HTML prototypes and database export files used during development.

The system replaces spreadsheet-based risk registers with a secure, centralised platform that provides:

- Asset Management
- Risk Register Management
- Risk Mitigation Tracking
- Audit Logging
- Role-Based Access Control (RBAC)
- Reporting and Exporting
- ISO 27001 Annex A Control Mapping

The application code in this repository primarily uses:

- Python 3 / Django
- PostgreSQL (schema / dumps included)
- Bootstrap 5 / HTML / CSS / JavaScript
- ReportLab (PDF generation helpers)

---

# Repository contents (high level)

At the repository root you will find application code, database dumps, and a number of support directories:

- .github/ — GitHub workflow and configuration
- ai/ — AI or experiment notes and resources
- templates/ — HTML templates and static prototype pages
  - templates/risk_whisperers/README.md documents the static HTML prototypes included
- risk_whisperers/ — Django app (views, models, templates)
- users/ — Django app for user management
- webapp/ — additional web application assets (if present)
- static/ — shared static files (css, js, images)
- scripts/ — helper scripts used during development
- manage.py — Django management entrypoint
- requirements.txt — Python dependencies
- Dockerfile / .dockerignore — container configuration
- database_schema.sql, risksys_db2.sql, backup.json — database schema and dumps

---

# Quickstart (development)

Clone the repository:

```bash
git clone https://github.com/Uric01/Risk-Whisperers.git
cd Risk-Whisperers
```

Create and activate a Python virtual environment (example):

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Configure the database (PostgreSQL) and update settings in the Django settings module. Example settings snippet:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "risksys_db",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser for the admin interface:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the app in your browser at:

http://127.0.0.1:8000/

---

# Notes about the templates/ directory

The repository contains a set of static HTML prototypes maintained in `templates/risk_whisperers/`. Those files are simple HTML mockups and include comments indicating backend work required for a Flask/Django port. There are also legacy/prototype files referencing a PHP implementation — these are included for reference only.

---

# Technologies used

- Python 3
- Django
- PostgreSQL
- Bootstrap 5
- HTML5 / CSS3 / JavaScript
- ReportLab
- Docker
- Git / GitHub

---

# Security features (high-level)

- Authentication
- Role-Based Access Control
- CSRF protections (Django)
- Secure ORM queries and server-side validation
- Audit logging and integrity constraints

---

# Future improvements (examples)

- Multi-factor Authentication (MFA)
- Email notifications
- Risk heat maps and analytics
- REST API endpoints
- Asset import/export and backup/restore
- Cloud deployment and CI/CD automation

---

# Testing

This project includes unit and system testing plus manual functional testing steps. The repository also contains exported SQL data and schema files to help with integration testing.

---

# Author

**Zweli Mashego**

Final Year BSc Information Technology (Software Engineering)

Richfield Graduate Institute of Technology

---

# Licence

This project was developed for academic purposes as part of a final-year BSc Information Technology research project.
