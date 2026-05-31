from django.http import Http404
from django.shortcuts import render

ALLOWED_PAGES = {
    'dashboard': 'dashboard.html',
    'assets': 'assets.html',
    'risks': 'risks.html',
    'add_asset': 'add_asset.html',
    'add_risk': 'add_risk.html',
    'add_mitigation': 'add_mitigation.html',
    'reports': 'reports.html',
    'audit_logs': 'audit_logs.html',
    'login': 'login.html',
}


def home(request):
    return render(request, 'login.html')


def page(request, page_name):
    template = ALLOWED_PAGES.get(page_name)
    if not template:
        raise Http404('Page not found')
    return render(request, template)
