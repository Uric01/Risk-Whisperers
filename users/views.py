from urllib import request

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model


def index(request):
     return render(request,"templates/risk_whisperers/login.html")
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        return redirect('index')
    
       # if user is not None:
        #    login(request, user)
            
            # Route to appropriate dashboard based on group
            #if user.groups.filter(name='Admin').exists() or user.is_staff:
            #    return render(request, 'users/dashboard.html')
            #elif user.groups.filter(name='Auditor').exists():
            #    return render(request, 'users/audit_logs.html')
            #elif user.groups.filter(name='Risk_Manager').exists():
            #    return render(request, 'risk_whisperers/add_risk.html')
            #
            # Default redirect
            
        #else:
       #     return render(request, 'users/login.html', {"error": "Invalid username or password"})
    
    #return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect("login")