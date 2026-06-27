from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def index(request):
     return redirect('page', 'login')

def login_view(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, username=username, password=password
            )
        
        # Redirect to the dashboard page after successful login
        if  user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('page', 'dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'risk_whisperers/login.html',{"message": messages})

def logout_view(request):
    logout(request)
    return render(request, 'risk_whisperers/login.html')
