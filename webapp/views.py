from django.http import Http404
from django.shortcuts import render

ALLOWED_PAGES = {
    'dashboard': 'risk_whisperers/dashboard.html',
    'assets': 'risk_whisperers/assets.html',
    'risks': 'risk_whisperers/risks.html',
    'add_asset': 'risk_whisperers/add_asset.html',
    'add_risk': 'risk_whisperers/add_risk.html',
    'add_mitigation': 'risk_whisperers/add_mitigation.html',
    'reports': 'risk_whisperers/reports.html',
    'audit_logs': 'risk_whisperers/audit_logs.html',
    'login': 'risk_whisperers/login.html',
    'edit_asset': 'risk_whisperers/edit_asset.html',
    'edit_risk': 'risk_whisperers/edit_risk.html',
    'edit_mitigation': 'risk_whisperers/edit_mitigation.html',
    'user_management': 'risk_whisperers/user_management.html',
    'index': 'risk_whisperers/index.html',
    'reports': 'risk_whisperers/reports.html',
    'report_print': 'risk_whisperers/report_print.html',
    'view_risk': 'risk_whisperers/view_risk.html',
    'view_asset': 'risk_whisperers/view_asset.html',
    'mitigations': 'risk_whisperers/mitigations.html',
}


def home(request):
    return render(request, ALLOWED_PAGES['login'])

def page(request, page_name):
    template = ALLOWED_PAGES.get(page_name)
    if not template:
        raise Http404('Page not found')
    user = request.user
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
    }
    return render(request, template, context)
