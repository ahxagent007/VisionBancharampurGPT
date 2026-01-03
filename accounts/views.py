from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return redirect("accounts:login")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("accounts:dashboard")
        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def dashboard(request):
    role = request.user.role
    if role == "ADMIN":
        return render(request, "accounts/dashboard_admin.html")
    if role == "STAFF":
        return render(request, "accounts/dashboard_staff.html")
    return render(request, "accounts/dashboard_member.html")
