from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse(reverse("login"))
    return render(request, 'users/login.html')
    
def login_view(request):
    # Handle login logic here
    if request.method == 'POST':
        username = request.POST.get('username')
        password =  request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'risk_whisperers/dashboard.html')
        else:
            return render(request, 'users/login.html', {"error": "Invalid username or password"})
        
    
    

def logout_view(request):
    # Handle logout logic here
    logout(request)
    return HttpResponse(reverse("index"))