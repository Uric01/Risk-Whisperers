from urllib import request

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.contrib import messages


def index(request):
     return render(request,"risk_whisperers/login.html")
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
          # Redirect to the dashboard page after successful login
    
        if user is not None:
           login(request, user)
           messages.success(request, "Login successful.")
           return render(request, 'risk_whisperers/dashboard.html')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'risk_whisperers/login.html')
    return render(request, 'risk_whisperers/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'risk_whisperers/login.html')