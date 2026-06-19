# Python porting notes (Flask / Django)

Static HTML prototypes in this folder map 1:1 to the PHP app. When converting to Python:

## Shared backend modules

| PHP file | Python equivalent |
|----------|-------------------|
| `config.php` | `.env` + `config.py` (DATABASE_URL) |
| `includes/db.php` | SQLAlchemy engine / Django ORM |
| `includes/auth.php` | `login_required`, `admin_required` decorators; Flask session or Django auth |
| `includes/helpers.php` | `services/report_service.py` — filter builders and summary queries |

## Routes (Flask example)

```
GET  /                          → redirect login or dashboard
GET|POST /login                 → login.html
GET  /logout                    → clear session, redirect login
GET  /dashboard                 → dashboard.html
GET  /assets                    → assets.html (filters)
GET|POST /assets/new            → add_asset.html
GET  /assets/<id>               → view_asset.html
GET|POST /assets/<id>/edit      → edit_asset.html
GET  /risks                     → risks.html
GET|POST /risks/new             → add_risk.html
GET  /risks/<id>                → view_risk.html
GET|POST /risks/<id>/edit       → edit_risk.html
GET  /mitigations               → mitigations.html
GET|POST /mitigations/new       → add_mitigation.html
GET|POST /mitigations/<id>/edit → edit_mitigation.html
GET  /reports                   → reports.html
GET  /reports/export            → CSV or report_print.html (PDF)
GET  /audit-logs                → audit_logs.html (admin only)
GET: load asset_categories, operational_statuses, information_classifications, asset_criticalities from DB
POST: validate asset_name, category_id, owner, asset_criticality required
INSERT into assets including asset_criticality
```

## Templates

- Extract repeated navbar from any page into `templates/partials/navbar.html`
- Use `{% extends "base.html" %}` and `{% block content %}`
- Replace `<!-- PYTHON: ... -->` with real Jinja2/Django template tags
- Add `{{ csrf_token() }}` on every POST form

## Security

- Password hashing: `werkzeug.security` or Django `make_password`
- Escape output: Jinja2 auto-escape / Django `{{ var }}`
- Role checks on every admin route and in templates for buttons

## Audit log

Call `audit_log(user_id, action, entity, entity_id, details, ip)` after CREATE/UPDATE/LOGIN.

## Risk Matrix function - to show badge on dashboard in risk table (currently javascript)
def get_risk_rating(score):
    if score >= 20:
        return ("Critical", "bg-danger")
    elif score >= 15:
        return ("High", "bg-danger")
    elif score >= 10:
        return ("Medium", "bg-warning text-dark")
    else:
        return ("Low", "bg-success")

# when building the risk list:
for risk in risks:
    risk["rating_text"], risk["rating_class"] = get_risk_rating(risk["rating"])

# Then in the html page
<td>
    <span class="badge {{ risk.rating_class }}">
        {{ risk.rating_text }} ({{ risk.rating }})
    </span>
</td>

## Future Enhancements (Not Required for MVP)

- Asset Criticality
- Risk Category
- Risk Owner
- Risk Due Date
- Risk Review Date
- Risk Trend (Increasing / Stable / Decreasing)
- Control Effectiveness
- Risk Acceptance Workflow
- Dashboard Charts
