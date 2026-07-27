# RiskSys – Web-Based Asset Risk Management System

## Project Overview

**RiskSys** is a web-based Asset Risk Management System developed as a final-year BSc Information Technology (Software Engineering) project. The application enables organisations to identify, assess, monitor, and mitigate risks associated with organisational assets while supporting the principles of **ISO/IEC 27001** and **ISO/IEC 27005**.

The system replaces traditional spreadsheet-based risk registers with a secure, centralised platform that provides:

- Asset Management
- Risk Register Management
- Risk Mitigation Tracking
- Audit Logging
- Role-Based Access Control (RBAC)
- Reporting and Exporting
- ISO 27001 Annex A Control Mapping

The application is built using:

- **Python 3**
- **Django**
- **PostgreSQL**
- **Bootstrap 5**
- **HTML5**
- **CSS3**
- **JavaScript**
- **ReportLab (PDF Generation)**

---

# Features

## Dashboard

The dashboard provides a real-time overview of the organisation's security posture, including:

- Total Assets
- Total Risks
- Open Risks
- Completed Mitigations
- Overdue Mitigations
- Recent High-Risk Items

---

## Asset Management

The Asset Register allows users to:

- Create assets
- View assets
- Edit assets
- Search assets
- Filter by:
  - Asset Category
  - Operational Status
- Classify assets according to:

  - Confidentiality
  - Integrity
  - Availability (CIA)

Each asset stores:

- Asset Name
- Description
- Owner
- Location
- Classification
- Operational Status
- Criticality
- CIA Ratings

---

## Risk Management

The Risk Register enables users to:

- Add risks
- View risks
- Edit risks
- Search risks
- Filter by:
  - Asset
  - Status
  - Description

Each risk records:

- Associated Asset
- Risk Description
- Risk Category
- Likelihood (1–5)
- Impact (1–5)
- Automatically Calculated Risk Rating
- Risk Treatment
- Risk Owner
- Review Date
- ISO 27001 Annex A Controls

---

## Mitigation Management

Users can create and manage mitigation plans for risks.

Each mitigation contains:

- Action Description
- Assigned User
- Target Date
- Progress Status
- Comments
- Effectiveness Review Date

Progress statuses include:

- Not Started
- In Progress
- Completed

---

## Reports

The reporting module supports:

- Date filtering
- Asset category filtering
- Risk status filtering

Generated reports display:

- Asset Category
- Asset Name
- Risk ID
- Risk Rating
- Risk Status
- Mitigation Target Date

Reports can be exported as:

- CSV (Excel compatible)
- PDF

The PDF report includes:

- Report metadata
- Applied filters
- Dashboard summary
- Risk breakdown table

---

## Audit Logs

Every important system action is recorded in an immutable audit trail.

Logged actions include:

- Login
- Asset Creation
- Asset Update
- Risk Creation
- Risk Update
- Mitigation Creation
- Mitigation Update

Audit logs can be filtered by:

- User
- Action Type
- Date Range

---

## Role-Based Access Control (RBAC)

The application supports four user roles.

### Administrator

Can:

- Manage users
- Create assets
- Edit assets
- Create risks
- Edit risks
- Create mitigations
- Edit mitigations
- View reports
- Export reports
- View audit logs

---

### Risk Manager

Can:

- Manage assets
- Manage risks
- Manage mitigations
- Generate reports

---

### Asset Owner

Can:

- View assigned assets
- View associated risks
- Manage assigned mitigations

---

### Auditor / Viewer

Can:

- View assets
- View risks
- View reports
- View audit logs

No modification permissions are granted.

---

# ISO/IEC 27001 Compliance

The system incorporates several ISO/IEC 27001 security management practices, including:

- Asset Classification
- CIA Classification
- Risk Assessment
- Risk Treatment
- Annex A Control Mapping
- Audit Logging
- Access Control
- Accountability
- Security Monitoring

---

# Project Structure

```
RiskSys/
│
├── risk_whisperers/
│   ├── templates/
│   │   └── risk_whisperers/
│   │       ├── dashboard.html
│   │       ├── assets.html
│   │       ├── add_asset.html
│   │       ├── edit_asset.html
│   │       ├── view_asset.html
│   │       ├── risks.html
│   │       ├── add_risk.html
│   │       ├── edit_risk.html
│   │       ├── view_risk.html
│   │       ├── mitigations.html
│   │       ├── add_mitigation.html
│   │       ├── edit_mitigation.html
│   │       ├── reports.html
│   │       ├── report_print.html
│   │       ├── audit_logs.html
│   │       ├── user_management.html
│   │       ├── login.html
│   │       └── index.html
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── migrations/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/<your-username>/RiskSys.git
```

```bash
cd RiskSys
```

---

## Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configure the database

Create a PostgreSQL database.

Update **settings.py**

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

---

## Apply migrations

```bash
python manage.py migrate
```

---

## Create an administrator account

```bash
python manage.py createsuperuser
```

---

## Start the development server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

# Technologies Used

- Python 3
- Django
- PostgreSQL
- Bootstrap 5
- HTML5
- CSS3
- JavaScript
- ReportLab
- Git
- GitHub

---

# Security Features

The application includes multiple security controls:

- Authentication
- Role-Based Access Control
- Django CSRF Protection
- Secure ORM Queries
- Input Validation
- Audit Logging
- Login Protection
- Database Integrity Constraints
- Foreign Key Enforcement
- Server-side Validation

---

# Future Enhancements

Planned improvements include:

- Multi-factor Authentication (MFA)
- Email Notifications
- Risk Heat Maps
- ISO 27001 Compliance Dashboard
- REST API
- Dashboard Analytics
- Asset Import/Export
- Automated Risk Scoring
- Backup and Restore
- Cloud Deployment
- AI-assisted Risk Recommendations
- Risk Trend Visualisations

---

# Testing

The project includes:

- Unit Testing
- System Testing
- Manual Functional Testing
- CRUD Validation
- Role-Based Access Control Testing
- Report Generation Testing
- Audit Log Verification

---

# Author

**Zweli Mashego**

Final Year BSc Information Technology (Software Engineering)

Richfield Graduate Institute of Technology

---

# Licence

This project is developed for academic purposes as part of a final-year BSc Information Technology research project.
