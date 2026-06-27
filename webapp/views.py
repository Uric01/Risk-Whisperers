from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from users.models import Asset, Risk, Mitigation
from django.contrib.auth.models import User



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


all_assets = Asset.objects.all()
all_risks = Risk.objects.all()
all_mitigations = Mitigation.objects.all()


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
        "risks": all_risks,
        "assets": all_assets,
        
    }
    return render(request, template, context)

#Add Asset
def add_asset(request):
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
        print(f"Asset saved with ID: {new_asset.asset}")
        return redirect('page', page_name='assets')
    
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



def assets_filter(request):
    all_assets = Asset.objects.all()
    q = request.GET.get("q")
    category = request.GET.get("category")
    status = request.GET.get("status")

    if q:
        all_assets = all_assets.filter(asset_name__icontains=q)

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


#Add Risk
def add_risk(request):
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
        "risks": all_risks,
    }
    return render(request, ALLOWED_PAGES['add_risk'], context)

def view_asset(request, asset_id):
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


def edit_asset(request, asset_id):
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
        
        # Redirect back to the view page to see the updates
        return redirect('view_asset', asset_id=selected_asset.asset)

    # For a GET request, pass the asset and permissions to the template
    user = request.user
    context = {
        "asset": selected_asset,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        # ... include your other role checks ...
    }
    
    return render(request, ALLOWED_PAGES['edit_asset'], context)


def add_risk(request):
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



def edit_risk(request, asset_id):
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
        
        # Redirect back to the view page to see the updates
        return redirect('view_asset', asset_id=selected_asset.asset)

    # For a GET request, pass the asset and permissions to the template
    user = request.user
    context = {
        "asset": selected_asset,
        "is_admin": user.groups.filter(name="Admin").exists() if user.is_authenticated else False,
        # ... include your other role checks ...
    }
    
    return render(request, ALLOWED_PAGES['edit_asset'], context)


def add_mitigation(request):
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

def view_mitigations(request):
    
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

def edit_mitigation(request, mitigation_id):
    asset_owners = User.objects.filter(groups__name="Asset_Owner").values_list('username', flat=True)
    asset_owner_list = list(asset_owners)
    
    # Fetch the existing mitigation action
    selected_mitigation = get_object_or_404(Mitigation, pk=mitigation_id)

    if request.method == "POST":
        # Update the object with new data from the form
        # Matches <select name="risk_id">
        selected_mitigation.risk_id = request.POST.get("risk_id") 
        
        # Matches <textarea name="action_description">
        selected_mitigation.action_description = request.POST.get("action_description")
        
        # Matches <select name="assigned_to">. Note: If this is a foreign key, 
        # Django usually expects the attribute to be assigned_to_id
        selected_mitigation.assigned_to_id = request.POST.get("assigned_to")
        
        # Matches <input name="target_date">
        selected_mitigation.target_date = request.POST.get("target_date")
        
        # Matches <select name="mitigation_status_id">
        selected_mitigation.status_id = request.POST.get("mitigation_status_id")
        
        # Matches <textarea name="comments">
        selected_mitigation.comments = request.POST.get("comments")
        
        # Matches <input name="effectiveness_review_date">
        selected_mitigation.effectiveness_review_date = request.POST.get("effectiveness_review_date")
        
        # Save the changes to the database
        selected_mitigation.save()
        
        # Redirect back to the mitigations view or wherever appropriate
        return redirect('page', page_name='mitigations') 

    # For a GET request, pass the mitigation and permissions to the template
    user = request.user
    is_auth = user.is_authenticated
    
    # Passing the exact booleans expected by your HTML template's logic
    context = {
        "mitigation": selected_mitigation,
        "is_admin": user.groups.filter(name="Admin").exists() if is_auth else False,
        "is_risk_manager": user.groups.filter(name="Risk Manager").exists() if is_auth else False,
        "is_auditor": user.groups.filter(name="Auditor").exists() if is_auth else False,
        "is_viewer": user.groups.filter(name="Viewer").exists() if is_auth else False,
        "is_owner": user.groups.filter(name="Owner").exists() if is_auth else False,
        "owners": asset_owner_list,
    }
    
    return render(request, ALLOWED_PAGES['edit_mitigation'], context)