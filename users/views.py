from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from webapp.views import log_event
from users.models import Asset, Risk, Mitigation, AuditLog, ActionType
from django.contrib.auth.models import User

def index(request):
     return redirect('page', 'login')

def login_view(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return redirect('login')
        
        user = authenticate(
            request, username=username, password=password
            )
        
        # Redirect to the dashboard page after successful login
        if  user is not None:
            
            login(request, user)
            
            log_event(
            request.user, 
            ActionType.LOGIN, 
            'Login', 
            request.user.id, 
            f"Logged in as: {request.user}"
            )
            return redirect('page', 'dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'risk_whisperers/login.html',{"message": messages})

def logout_view(request):
    messages.success(request, f"You have been logged out.")
    log_event(
            request.user, 
            ActionType.LOGOUT, 
            'Logout', 
            request.user.id, 
            f"{request.user} logged out"
            )
    logout(request)
    
    return render(request, 'risk_whisperers/login.html')
