from urllib import request

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    # Redirect authenticated users to appropriate dashboard
    if request.user.groups.filter(name='Risk_Manager').exists():
        return render(request, 'users/add_risk.html')
    elif request.user.groups.filter(name='Auditor').exists():
        return redirect('audit_logs')
    elif request.user.groups.filter(name='Admin').exists() or request.user.is_staff:
        return redirect('dashboard')
    
    # Default redirect if user has no groups
    return redirect('dashboard')
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Route to appropriate dashboard based on group
            if user.groups.filter(name='Risk_Manager').exists():
                return render(request, 'risk_whisperers/add_risk.html')
            elif user.groups.filter(name='Auditor').exists():
                return render(request, 'users/audit_logs.html')
            elif user.groups.filter(name='Admin').exists() or user.is_staff:
                return render(request, 'users/dashboard.html')
            
            # Default redirect
            return redirect('index')
        else:
            return render(request, 'users/login.html', {"error": "Invalid username or password"})
    
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect("login")