import csv
from io import BytesIO, StringIO
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from users.models import Asset, Risk, Mitigation, AuditLog, ActionType, OperationalStatus
from django.contrib.auth.models import User
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Min



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

report_data = [
    {
        "category": m.risk.asset.asset_category,
        "asset": m.risk.asset.asset_name,
        "risk_id": m.risk.risk_id,
        "rating": m.risk.risk_rating,
        "status": m.risk.risk_status,
        "target_date": m.target_date,
    }
    for m in Mitigation.objects.select_related("risk", "risk__asset")
]
@login_required
def home(request):
    return render(request, ALLOWED_PAGES['login'])

@login_required
def page(request, page_name):
    all_assets = Asset.objects.all()
    all_risks = Risk.objects.all()
    all_mitigations = Mitigation.objects.all()
    all_asset_categories = Asset.objects.values_list("asset_category", flat=True)
    all_risks_statuses = Risk.objects.values_list("risk_status", flat=True)

    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    all_auditlog = AuditLog.objects.all().order_by('-action_date')
    
    asset_owners = User.objects.filter(groups__name="Asset_Owner").values_list('username', flat=True)
    asset_owner_list = list(asset_owners)
    template = ALLOWED_PAGES.get(page_name)
    total_assets = all_assets.count()
    total_risks = all_risks.count()
    total_open_risks = all_risks.filter(risk_status="OPEN").count()
    total_completed_mitigations = all_mitigations.filter(progress_status="Completed").count()
    overdue_mitigations_count =  count
    
    if not template:
        raise Http404('Page not found')
    user = request.user
    all_users = User.objects.all()
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "risks": all_risks,
        "assets": all_assets,
        "mitigations":all_mitigations,
        "owners": asset_owner_list,
        "asset_categories":all_asset_categories,
        "all_risks_statuses":all_risks_statuses,
        "total_assets":total_assets,
        "total_risks": total_risks,
        "total_open_risks": total_open_risks,
        "overdue_mitigations_count": overdue_mitigations_count,
        "report_data":report_data,
        "total_completed_mitigations":total_completed_mitigations,
        'all_auditlogs': all_auditlog,
        'all_users': all_users,
    }
    return render(request, template, context)

#Add Asset
@login_required
def add_asset(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1

    if request.method == "POST":
        new_asset = Asset.objects.create(
            asset_name=request.POST.get("asset_name"),
            asset_description=request.POST.get("asset_description"),
            asset_owner=request.POST.get("asset_owner"),
            location=request.POST.get("asset_location"),
            asset_criticality=request.POST.get("asset_criticality"),
            cia_confidentiality=request.POST.get("confidentiality_impact"),
            cia_integrity=request.POST.get("integrity_impact"),
            cia_availability=request.POST.get("availability_impact"),
            asset_category=request.POST.get("asset_category"),
            operational_status=request.POST.get("operational_status"),
            classification=request.POST.get("classification"),
            
        )
         # Log the generation
        log_event(
            request.user, 
            ActionType.CREATE, 
            'Asset', 
            new_asset.asset, 
            f"Created new asset: {new_asset.asset_name}"
            )
        print(f"Asset saved with ID: {new_asset.asset}")
        user = request.user
        context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets":all_assets,
    }
        return render(request,ALLOWED_PAGES['assets'],context)
    
    # FIXED: Render the page directly for GET requests instead of redirecting
    user = request.user
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
    }
    return render(request, ALLOWED_PAGES['add_asset'], context)


@login_required
def assets_filter(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    q = request.GET.get("q")
    category = request.GET.get("category")
    status = request.GET.get("status")

    if q:
        all_assets =  all_assets.filter( Q(asset_description__icontains=q) |
        Q(asset_category__icontains=q) |
        Q(asset_owner__icontains=q) |
        Q(location__icontains=q) | 
        Q(operational_status__icontains=q))

    if category:
        all_assets = all_assets.filter(asset_category=category)

    if status:
        all_assets = all_assets.filter(operational_status=status)
    
    if category and status:
        all_assets = all_assets.filter(asset_category=category).filter(operational_status=status)
        
    if q and category and status:
        all_assets = all_assets.filter(asset_category=category).filter(operational_status=status).filter(asset_name__icontains=q)
        
    if q and category:
        all_assets = all_assets.filter(asset_category=category).filter(asset_name__icontains=q)

    if q and status:
        all_assets = all_assets.filter(operational_status=status).filter(asset_name__icontains=q)

    user = request.user
    
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets # FIXED: Changed from "asset_filter"
    }
    
    print("TOTAL ASSETS:", all_assets.count())

    return render(request, ALLOWED_PAGES['assets'], context)



@login_required
def audit_log_filter(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    # Grab the values from the HTML form
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    user_id = request.GET.get("user_id")
    action_type = request.GET.get("action_type")
    all_auditlogs = AuditLog.objects.select_related("user").all().order_by('-action_date')
    earliest_date = all_auditlogs.aggregate(Min('action_date'))['action_date__min']

    # 3. Apply the Date Filters
    if date_from:
        # Converts the DateTime in the DB to a Date for accurate comparison
        all_auditlogs = all_auditlogs.filter(action_date__date__gte=date_from)

    if date_to:
        all_auditlogs = all_auditlogs.filter(action_date__date__lte=date_to)

    # 4. Apply the other filters while we are at it!
    if action_type:
        all_auditlogs = all_auditlogs.filter(action_type=action_type)

    if user_id:
        all_auditlogs = all_auditlogs.filter(user_id=user_id)

    user = request.user
    all_users = User.objects.all()

    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets,
        "all_auditlogs": all_auditlogs,
        "all_users": all_users,
        "selected_user_id": user_id or "",
        "selected_action_type": action_type or "",
        "selected_date_from": date_from or "",
        "selected_date_to": date_to or "",
        "current_date": current_date,
        "earliest_date": earliest_date,
    }
    
    print("TOTAL ASSETS:", all_assets.count())

    return render(request, ALLOWED_PAGES['audit_logs'], context)





@login_required
def view_asset(request, asset_id):
    
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    selected_asset = get_object_or_404(Asset, asset=asset_id)
    
    user = request.user
    context = {
        "asset": selected_asset,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
    }
    
    return render(request, ALLOWED_PAGES['view_asset'], context)

@login_required
def edit_asset(request, asset_id):
    
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    # Fetch the existing asset
    selected_asset = get_object_or_404(Asset, asset=asset_id)

    if request.method == "POST":
        # Update the object with new data from the form
        selected_asset.asset_name = request.POST.get("asset_name")
        selected_asset.asset_description = request.POST.get("asset_description")
        selected_asset.asset_owner = request.POST.get("asset_owner")
        selected_asset.location = request.POST.get("asset_location")
        
        # Make sure your HTML name attributes match what you expect here!
        selected_asset.asset_category = request.POST.get("asset_category")
        selected_asset.operational_status = request.POST.get("operational_status")
        selected_asset.classification = request.POST.get("classification")
        selected_asset.cia_confidentiality = request.POST.get("confidentiality_impact")
        selected_asset.cia_integrity = request.POST.get("integrity_impact")
        selected_asset.cia_availability = request.POST.get("availability_impact")
        
        # Save the changes to the database
        selected_asset.save()
        
        log_event(
        request.user,
        ActionType.UPDATE,
        'Asset',
        selected_asset.asset, 
        f"Modified asset for Asset ID {selected_asset.asset}. Status set to: {selected_asset.operational_status}"
    )
        
        # Redirect back to the view page to see the updates
        return redirect('view_asset', asset_id=selected_asset.asset)

    # For a GET request, pass the asset and permissions to the template
    user = request.user
    context = {
        "asset": selected_asset,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
    }
    return render(request, ALLOWED_PAGES['edit_asset'], context)




@login_required
def add_asset_risk(request, asset_id):
    
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    # Fetch the existing asset
    selected_asset = get_object_or_404(Asset, asset=asset_id)

    user = request.user
    context = {
        "selected_asset": selected_asset,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
    }
    return render(request, ALLOWED_PAGES['add_risk'], context)

@login_required
def add_risk(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    if request.method == "POST":
        asset_id = request.POST.get("asset")
        selected_asset = Asset.objects.get(asset=asset_id)
        new_risk = Risk.objects.create(
            asset=selected_asset,
            risk_description=request.POST.get("risk_description"),
            risk_category=request.POST.get("risk_category"),
            likelihood=request.POST.get("likelihood"),
            impact=request.POST.get("impact"),
            risk_rating=request.POST.get("risk_rating"),
            risk_status=request.POST.get("risk_status"),
            risk_treatment=request.POST.get("risk_treatment_option"),
            risk_owner=request.POST.get("risk_owner"),
            review_date=request.POST.get("review_date"),
            annex_control=request.POST.get("control"),
           
        )
        
        log_event(
            request.user, 
            ActionType.CREATE, 
            'Risk', 
            new_risk.risk_id, 
            f"Created new risk: {new_risk.risk_description}"
            )
        print(f"Asset saved with ID: {new_risk.asset}")
        return redirect('page', page_name='risks')

    user = request.user
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets":all_assets,
    }
    return render(request, ALLOWED_PAGES['add_risk'], context)


@login_required
def edit_risk(request, risk_id):
    
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    # Fetch the existing asset
    selected_risk = get_object_or_404(Risk, risk_id=risk_id)

    if request.method == "POST":
        # Update the object with new data from the form
        selected_risk.risk_description = request.POST.get("risk_description")
        selected_risk.likelihood = request.POST.get("likelihood")
        selected_risk.impact = request.POST.get("impact")
        selected_risk.risk_rating = request.POST.get("risk_rating")
        selected_risk.risk_status = request.POST.get("risk_status")
        selected_risk.risk_treatment = request.POST.get("risk_treatment")
        selected_risk.review_date = request.POST.get("review_date")
        selected_risk.annex_control = request.POST.get("annex_control")
        
        # Save the changes to the database
        selected_risk.save()
        
        # Log the modification
        log_event(
            request.user, 
            ActionType.UPDATE, 
            'Risk', 
            selected_risk.risk_id, 
            f"Updated Risk ID {selected_risk.risk_id} (Rating: {selected_risk.risk_rating})"
        )
        
        # Redirect back to the risk page to see the updates
        return redirect('view_risk', risk_id=selected_risk.risk_id)


    user = request.user
    context = {
        "selected_risk": selected_risk,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
    }
    
    
    return render(request, ALLOWED_PAGES['edit_risk'], context)




@login_required
def risk_filter(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    all_risks = Risk.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    q = request.GET.get("q")
    asset_name_ = request.GET.get("asset_name_")
    risk_status = request.GET.get("risk_status")

    if q:
        all_risks = all_risks.filter( Q(risk_description__icontains=q) |
        Q(risk_owner__icontains=q) |
        Q(risk_status__icontains=q) |
        Q(asset__asset_name__icontains=q))

    if asset_name_:
        all_assets = all_assets.filter(asset_name=asset_name_)

    if risk_status:
        all_risks = all_risks.filter(risk_status=risk_status)
    
    if q and risk_status:
        all_risks = all_risks.filter(risk_description__icontains=q).filter(risk_status=risk_status)
        

    user = request.user
    
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets, # FIXED: Changed from "asset_filter"
        "risks" : all_risks,
    }
    
    print("TOTAL ASSETS:", all_assets.count())

    return render(request, ALLOWED_PAGES['risks'], context)



@login_required
def view_risk(request, risk_id):
    
    all_assets = Asset.objects.all()
    all_risks = Risk.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    selected_risk = get_object_or_404(Risk, risk_id=risk_id)
    
    user = request.user
    context = {
        "selected_risk": selected_risk,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "risks": all_risks,
        "assets": all_assets,
        "mitigations":all_mitigations,
    }
    
    return render(request, ALLOWED_PAGES['view_risk'], context)

@login_required
def view_risk_edit(request, risk_id):
    
    all_assets = Asset.objects.all()
    all_risks = Risk.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    selected_risk_to_edit = get_object_or_404(Risk, risk_id=risk_id)
    
    user = request.user
    context = {
        "selected_risk_to_edit": selected_risk_to_edit,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "risks": all_risks,
        "assets": all_assets,
        "mitigations":all_mitigations,
    }
    
    return render(request, ALLOWED_PAGES['edit_risk'], context)


@login_required
def view_risk_add_mitigation(request, risk_id):
    
    all_assets = Asset.objects.all()
    all_risks = Risk.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    selected_risk_add_mitigation = get_object_or_404(Risk, risk_id=risk_id)
    
    user = request.user
    context = {
        "selected_risk_add_mitigation": selected_risk_add_mitigation,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "risks": all_risks,
        "assets": all_assets,
        "mitigations":all_mitigations,
    }
    
    return render(request, ALLOWED_PAGES['add_mitigation'], context)

@login_required
def add_mitigation(request):
    
    all_assets = Asset.objects.all()
    all_risks = Risk.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    asset_owners = User.objects.filter(groups__name="Asset_Owner").values_list('username', flat=True)
    asset_owner_list = list(asset_owners)
    
    if request.method == "POST":
        risk_id = request.POST.get("risk_id")
        selected_risk = Risk.objects.get(risk_id=risk_id)
        
        assigned_to_username = request.POST.get("assigned_to")
        
        try:
            assigned_user = User.objects.get(username=assigned_to_username)
        except User.DoesNotExist:
          
            assigned_user = None 
            
        new_mitigation = Mitigation.objects.create(
            risk=selected_risk,
            action_description=request.POST.get("action_description"),
            assigned_to=assigned_user,
            target_date=request.POST.get("target_date"),
            progress_status=request.POST.get("mitigation_status"),
            comments=request.POST.get("comments"),
            effectiveness_review_date=request.POST.get("effectiveness_review_date"),
        )
        
        log_event(
            request.user, 
            ActionType.CREATE, 
            'Mitigation', 
            new_mitigation.mitigation_id, 
            f"Created new mitigation: {new_mitigation.action_description}"
            )
        
        print(f"Mitigation saved with ID: {new_mitigation.pk}")
        user = request.user
        context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets,
        "mitigations": all_mitigations,
    }
        return render(request, ALLOWED_PAGES['mitigations'], context )

    user = request.user
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets,
        "mitigations": all_mitigations,
        "risks": all_risks,
        "owners": asset_owner_list,
    }
    return render(request, ALLOWED_PAGES['add_mitigation'], context)

@login_required
def view_mitigations(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    
    user = request.user
    
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets,
        "mitigations": all_mitigations,
    }
    return render(request, ALLOWED_PAGES['mitigations'], context)

def edit_risk_mitigation(request):
    
    all_assets = Asset.objects.all()
    all_mitigations = Mitigation.objects.all()
    target_dates = all_mitigations.values_list("target_date", flat=True)
    current_date = date.today()
    count = 0
    for target_date in target_dates:
        if current_date > target_date:
            count += 1
    all_auditlog = AuditLog.objects.all()
    
    asset_owners = User.objects.filter(groups__name="Asset_Owner").values_list('username', flat=True)
    asset_owner_list = list(asset_owners)
    if request.method == "POST":
        risk_id = request.POST.get("risk_id")
        #Fetch the selected risk to ensure it exists
        selected_risk = get_object_or_404(Risk, risk_id=risk_id)
        
        # Fetch the associated mitigation row using the risk foreign key
        # .first() safely grabs the mitigation, or returns None if none exists yet
        mitigation = Mitigation.objects.filter(risk=selected_risk).first()
        
        # If the user is submitting updates, ensure a mitigation actually exists to update
        if mitigation:
            mitigation.action_description = request.POST.get("action_description")
            mitigation.target_date = request.POST.get("target_date")
            mitigation.progress_status = request.POST.get("mitigation_status")
            mitigation.comments = request.POST.get("comments")
            mitigation.effectiveness_review_date = request.POST.get("effectiveness_review_date")
            
            # Handle the assigned_to foreign key
            assigned_to_username = request.POST.get("assigned_to")
            try:
                mitigation.assigned_to = User.objects.get(username=assigned_to_username)
            except User.DoesNotExist:
                pass # Handle user not found appropriately
                
            mitigation.save()
                
            log_event(
            request.user,
            ActionType.UPDATE,
            'Mitigation',
            mitigation.mitigation_id,
            f"Modified mitigation for Risk ID {mitigation.risk.risk_id}. Status set to: {mitigation.progress_status}"
        )
            return redirect('page', page_name='mitigations')

    # 3. For a GET request, pass the mitigation object to the template context
    user = request.user
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "assets": all_assets,
        "owners": asset_owner_list,
    }
    
    # Ensure this points to the correct HTML template for editing mitigations
    return render(request, ALLOWED_PAGES['edit_mitigation'], context)

@login_required
def report_filter(request):
    all_mitigations = Mitigation.objects.select_related("risk", "risk__asset").all()
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    category = request.GET.get("category")
    risk_status = request.GET.get("risk_status")

    if date_from:
        all_mitigations = all_mitigations.filter(target_date__gte=date_from)

    if date_to:
        all_mitigations = all_mitigations.filter(target_date__lte=date_to)

    if category:
        all_mitigations = all_mitigations.filter(risk__asset__asset_category=category)

    if risk_status:
        all_mitigations = all_mitigations.filter(risk__risk_status=risk_status)

    report_data = [
        {
            "category": mitigation.risk.asset.asset_category,
            "asset": mitigation.risk.asset.asset_name,
            "risk_id": mitigation.risk.risk_id,
            "rating": mitigation.risk.risk_rating,
            "status": mitigation.risk.risk_status,
            "target_date": mitigation.target_date,
        }
        for mitigation in all_mitigations
    ]

    current_date = date.today()
    overdue_mitigations_count = sum(1 for item in report_data if item["target_date"] < current_date and item["status"] != "CLOSED")

    all_assets = Asset.objects.all()
    all_risks = Risk.objects.all()
    all_risks_statuses = Risk.objects.values_list("risk_status", flat=True)
    asset_categories = Asset.objects.values_list("asset_category", flat=True)

    total_assets = all_assets.count()
    total_risks = all_risks.count()
    total_open_risks = all_risks.filter(risk_status="OPEN").count()

    user = request.user
    context = {
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        "is_risk_manager": user.groups.filter(name="Risk_Manager").exists() if user.is_authenticated else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if user.is_authenticated else False,
        "is_viewer": user.groups.filter(name="viewer").exists() if user.is_authenticated else False,
        "is_owner": user.groups.filter(name="Asset_Owner").exists() if user.is_authenticated else False,
        "report_data": report_data,
        "asset_categories": asset_categories,
        "all_risks_statuses": all_risks_statuses,
        "total_assets": total_assets,
        "total_risks": total_risks,
        "total_open_risks": total_open_risks,
        "overdue_mitigations_count": overdue_mitigations_count,
        "selected_date_from": date_from or "",
        "selected_date_to": date_to or "",
        "selected_category": category or "",
        "selected_risk_status": risk_status or "",
    }

    return render(request, ALLOWED_PAGES['reports'], context)


@login_required
def report_export(request, file_format):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    category = request.GET.get("category")
    risk_status = request.GET.get("risk_status")

    all_mitigations = Mitigation.objects.select_related("risk", "risk__asset").all()
    if date_from:
        all_mitigations = all_mitigations.filter(target_date__gte=date_from)
    if date_to:
        all_mitigations = all_mitigations.filter(target_date__lte=date_to)
    if category:
        all_mitigations = all_mitigations.filter(risk__asset__asset_category=category)
    if risk_status:
        all_mitigations = all_mitigations.filter(risk__risk_status=risk_status)

    report_rows = [
        {
            "category": mitigation.risk.asset.asset_category,
            "asset": mitigation.risk.asset.asset_name,
            "risk_id": f"RSK-{mitigation.risk.risk_id}",
            "rating": mitigation.risk.risk_rating,
            "status": mitigation.risk.risk_status,
            "target_date": mitigation.target_date,
        }
        for mitigation in all_mitigations
    ]

    if file_format == "excel":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Category", "Asset", "Risk ID", "Rating", "Status", "Target Date"])
        for row in report_rows:
            writer.writerow([row["category"], row["asset"], row["risk_id"], row["rating"], row["status"], row["target_date"]])

        response = HttpResponse(output.getvalue(), content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="risk_report.csv"'
        return response

    if file_format == "pdf":
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="risk_report.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5 * inch, leftMargin=0.5 * inch, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontSize = 16
        title_style.leading = 20
        body_style = styles['BodyText']
        body_style.fontSize = 9

        total_assets = Asset.objects.count()
        total_risks = Risk.objects.count()
        total_open_risks = Risk.objects.filter(risk_status='OPEN').count()
        overdue_mitigations_count = sum(1 for row in report_rows if row['target_date'] < date.today() and row['status'] != 'CLOSED')

        summary_data = [
            [Paragraph('<b>Total Assets</b><br/><font size=14>{}</font>'.format(total_assets)), Paragraph('<b>Total Risks</b><br/><font size=14>{}</font>'.format(total_risks))],
            [Paragraph('<b>Open Risks</b><br/><font size=14>{}</font>'.format(total_open_risks)), Paragraph('<b>Overdue Mitigations</b><br/><font size=14>{}</font>'.format(overdue_mitigations_count))],
        ]
        summary_table = Table(summary_data, colWidths=[2.7 * inch, 2.7 * inch], rowHeights=[0.7 * inch, 0.7 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))

        table_data = [["Category", "Asset", "Risk ID", "Rating", "Status", "Target Date"]]
        for row in report_rows:
            table_data.append([row['category'], row['asset'], row['risk_id'], row['rating'], row['status'], row['target_date']])

        table = Table(table_data, repeatRows=1, colWidths=[0.8 * inch, 1.4 * inch, 0.8 * inch, 0.6 * inch, 0.9 * inch, 1.0 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        exported_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exported_by = request.user.get_full_name() or request.user.username if request.user.is_authenticated else 'Anonymous'

        story = [
            Paragraph('Reports & Compliance View', title_style),
            Paragraph('Systemic risk report with filters and export.', body_style),
            Paragraph(f"Exported at: {exported_at}", body_style),
            Paragraph(f"Exported by: {exported_by}", body_style),
            Spacer(1, 0.1 * inch),
            Paragraph(
                f"Filters: Date From: {date_from or 'All'} | Date To: {date_to or 'All'} | Asset Category: {category or 'All'} | Risk Status: {risk_status or 'All'}",
                body_style,
            ),
            Spacer(1, 0.15 * inch),
            summary_table,
            Spacer(1, 0.2 * inch),
            table,
        ]
        doc.build(story)
        response.write(buffer.getvalue())
        return response

    return HttpResponse("Unsupported format", status=400)


def log_event(user, action_type, entity_name, entity_id, details):
    
    """
    Utility to record audit logs. 
    Only records if the user is authenticated.
    """
    if user.is_authenticated:
        AuditLog.objects.create(
            user=user,
            action_type=action_type,
            entity_name=entity_name,
            entity_id=str(entity_id),
            action_details=details
        )
        
    
