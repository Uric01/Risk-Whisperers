# Web-Based Asset Risk Management System (HTML Wireframes)

## Project Overview
This repository contains the front-end HTML wireframe implementation of a Web-Based Asset Risk Management System. It relies entirely on HTML, CSS, and minimal Javascript to prototype the complete user journey and layout logic before any backend integration (like PHP/MySQL) takes place.

The system is fully designed with **Bootstrap 5**, leveraging custom styling for a premium, dark mode aware aesthetic. Additionally, the system incorporates requirements for **ISO 27001 Information Security Management** directly into the capture forms.

## Files Structure
*   `login.html` - The entry point for the mock application.
*   `dashboard.html` - The central navigation hub displaying metric summaries.
*   `assets.html` / `add_asset.html` - Asset Register and capture forms, including ISO 27001 CIA classification logic.
*   `risks.html` / `add_risk.html` - Risk Register and capture forms, including ISO 27001 Risk Treatment mapping and dynamic impact calculators.
*   `add_mitigation.html` - Form to create mitigation steps, including ISO 27001 Effectiveness tracking.
*   `reports.html` - Filterable dashboards and summary reports.
*   `audit_logs.html` - Immutable audit log interface.
*   `style.css` - Custom styling overrides to provide a premium feel.
*   `auth.js` - Mock Authentication script for role-based testing.

## How to Test the Role-Based Mapping
A script (`auth.js`) automatically detects the role logged-in with to replicate a Role-Based Access Control (RBAC) system. The system natively supports **Admin** and **Read-Only** users.
Additional mapping needs to be made for this in HTML files to reference this, the js file is just for testing

1.  Open `login.html` in your web browser.
2.  **To test Admin access:** Enter `admin` as the username. This will give you full access to create assets, risks, and mitigations.
3.  **To test Read-Only Access:** Enter any other username (e.g., `viewer`) and any password. The system will mock a "Read-Only" session. Action buttons, write-interfaces, and restricted navigation items (like the raw registers) will be hidden from the Dashboard and Reports views. The user's name in the top right will change to reflect the Read-Only status.

## Future Implementation Notes
When integrating the backend later:
*   Remove `auth.js` and replace the display logic with your server-side session checks.
*   Connect the Dashboard metric cards to query `COUNT(*)` data points from the SQL database.
*   Extract the static `<nav>` bar into a server template file (like `header.php`) to unify navigation across all pages.

## TODO (Python + MySQL Backend Setup)

### MySQL setup
*   Create the MySQL database (see `database_schema.sql`) and run the schema to create `users`, `assets`, `risks`, `risk_controls`, `mitigations`, and `audit_logs`.
*   Ensure foreign keys are enabled and working (example: `risks.asset_id -> assets.asset_id`, `mitigations.risk_id -> risks.risk_id`, and optional `assigned_to -> users.user_id`).
*   Add an app database user (least-privilege) and grant only the required permissions for the backend to read/write the tables used by the UI.
*   Seed test data for development (users + a baseline set of assets/risks) so the dropdowns and dashboard metrics have results to display.

### Python backend setup
*   Set up a Python server (for example, FastAPI or Flask) and a DB connection layer using a MySQL driver (for example, SQLAlchemy or a MySQL connector).
*   Add configuration via environment variables (for example: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, and the backend host/port).
*   Implement authentication/authorization to replace `auth.js` (session/JWT).
*   Add a `/login` endpoint to validate user credentials and store a session/JWT.
*   Enforce RBAC so "Admin" can access write actions (add/update/delete) while "Read-Only" can only view.
*   Dashboard metrics endpoint (Python should query and return counts): total assets, total risks, open risks, and completed mitigations for `dashboard.html`.
*   Asset + risk fetch endpoints to support DB-driven dropdowns/tables across the UI:
    *   `GET /assets` for:
        *   `risks.html` filter dropdown (currently hardcoded options)
        *   `add_risk.html` selected asset context (currently hardcoded)
*   `GET /risks` with query params (for `risks.html` table + filters):
    *   `asset_id` (for "Filter by Asset...")
        *   `status` (Open/Mitigated/Closed)
        *   `search` (risk description search input)
    *   `GET /risks/:risk_id` (or equivalent) so `add_mitigation.html` can render the "Selected Risk" summary box based on the chosen risk.
    *   `GET /users` (Admin/assignable users) so `add_mitigation.html` can populate the `assignedTo` dropdown from the `users` table.
*   Risk creation flow for `add_risk.html`:
    *   Support passing an `asset_id` into `add_risk.html` (for example, via `?asset_id=...`) so the "Selected Asset" box/select can show the correct asset from DB.
    *   On `POST /risks`, persist:
        *   `asset_id`, `risk_description`, `likelihood`, `impact`, `risk_treatment`, `review_date`, `risk_status`
        *   selected `annexAControls` into `risk_controls` (one row per selected Annex A control code)
*   Mitigation creation flow for `add_mitigation.html`:
    *   Support passing a `risk_id` into `add_mitigation.html` (for example, via `?risk_id=...`) so the "Selected Risk" summary box can be populated from DB.
    *   On `POST /mitigations`, persist `risk_id`, `action_description`, `assigned_to`, `target_date`, `progress_status`, `comments`, and `effectiveness_review_date`.
*   Create endpoints used by the capture forms:
    *   `POST /assets` to create an asset from `add_asset.html`.
    *   `POST /risks` to create a risk from `add_risk.html` (including writing `risk_controls` rows).
    *   `POST /mitigations` to create a mitigation from `add_mitigation.html`.
*   Reports endpoints (for `reports.html`):
    *   Support filtering report output using the UI inputs: date range, asset category, and risk status.
    *   Provide an endpoint that returns:
        *   Dashboard-style counts (total assets filtered, total risks, open risks, overdue mitigations)
        *   The detailed “Risk breakdown” rows (category, asset name, risk id, rating, status, mitigation target date)
    *   Define report rules when a risk has multiple mitigations (recommended:
        treat the earliest `target_date` where `progress_status != 'Completed'` as the current mitigation target, and count it as overdue if `target_date < today` and not completed).
    *   Implement the “Generate Report” button to call the report endpoint and render rows dynamically.
    *   Implement export endpoints for the “Export PDF/Excel” buttons (or document that exports are a later phase).
*   Audit logs endpoints (for `audit_logs.html`):
    *   Provide an endpoint (admin-only) that returns audit logs with server-side filtering:
        *   filter by user (match `users.full_name`)
        *   action type (`CREATE`/`UPDATE`/`DELETE`/`LOGIN`)
        *   date range (`audit_logs.action_date`)
    *   Join `audit_logs` with `users` so the UI can show a user name (and display "System" when `user_id` is NULL).
    *   Sort by `audit_logs.action_date` (most recent first) and support pagination for large logs.
    *   Standardize on UTC for timestamps written to `audit_logs.action_date` (convert from server local time if needed) to match the “UTC” label in the UI.
*   Add audit logging in Python by writing to `audit_logs` on create/update/delete/login actions (linking actions to `users.user_id` when available).
*   Implement local development integration details by serving the backend on a stable port and configuring CORS (if the frontend is opened separately from the backend).
*   Define a small JSON API contract (request/response fields) and update each page's JavaScript to replace the current hardcoded table rows/dropdown options.
*   Update navigation/actions so pages pass selected IDs (for example, `add_risk.html?asset_id=...` and `add_mitigation.html?risk_id=...`) to drive the "Selected Asset/Risk" sections from the database.
*   Implement the remaining CRUD endpoints needed by the UI (for example, edit/view for risks and mitigation flows referenced by `risks.html` action buttons).
*   Implement real password hashing (for example bcrypt) when storing `users.password_hash`, and map `role` values correctly for RBAC.
