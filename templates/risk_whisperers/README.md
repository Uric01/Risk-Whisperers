# RiskSys — Static HTML prototypes

HTML-only mockups of every user-facing screen. Open files directly in a browser (Bootstrap CDN required for full styling).

**Stylesheet:** `../assets/style.css` (shared with the PHP app)

## Pages

| File | PHP equivalent |
|------|----------------|
| `index.html` | `index.php` |
| `login.html` | `login.php` |
| `dashboard.html` | `dashboard.php` |
| `assets.html` | `assets.php` |
| `add_asset.html` | `add_asset.php` |
| `view_asset.html` | `view_asset.php` |
| `edit_asset.html` | `edit_asset.php` |
| `risks.html` | `risks.php` |
| `add_risk.html` | `add_risk.php` |
| `view_risk.html` | `view_risk.php` |
| `edit_risk.html` | `edit_risk.php` |
| `mitigations.html` | `mitigations.php` |
| `add_mitigation.html` | `add_mitigation.php` |
| `edit_mitigation.html` | `edit_mitigation.php` |
| `reports.html` | `reports.php` |
| `report_print.html` | `report_export.php` (PDF/print view) |
| `audit_logs.html` | `audit_logs.php` |

Each file contains `<!-- PYTHON: ... -->` comments describing backend/template work for a Flask or Django port.
