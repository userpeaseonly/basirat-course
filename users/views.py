from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, QuickCreateAccountForm


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def create_account(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = QuickCreateAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = QuickCreateAccountForm()
    return render(request, "users/create_account.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    """
    Home page view - accessible to all authenticated users
    """
    context = {
        'user': request.user,
    }
    return render(request, "users/home.html", context)
