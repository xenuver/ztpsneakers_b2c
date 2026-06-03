from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from .models import User

def get_redirect_url_for_role(user):
    if user.role == 'admin_toko':
        return '/admin-toko/'
    elif user.role == 'owner' or user.is_superuser:
        return '/jasmine/'
    return '/'

def auth_view(request):
    if request.user.is_authenticated:
        return redirect(get_redirect_url_for_role(request.user))
    
    login_form = UserLoginForm()
    register_form = UserRegisterForm()
    
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': 'login'
    }
    return render(request, "userauths/auth.html", context)

def login_tab(request):
    """HTMX view to render just the login form."""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0) # Expire on browser close
                
                response = render(request, "userauths/partials/login_form.html", {"login_form": form})
                response['HX-Redirect'] = get_redirect_url_for_role(user)
                return response
            else:
                form.add_error(None, "Email atau kata sandi salah!")
    else:
        form = UserLoginForm()
        
    return render(request, "userauths/partials/login_form.html", {"login_form": form})

def register_tab(request):
    """HTMX view to render just the register form."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            password_confirm = form.cleaned_data.get("password_confirm")
            if password != password_confirm:
                form.add_error("password_confirm", "Password tidak cocok.")
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.role = 'customer'
                user.save()
                
                login(request, user)
                response = render(request, "userauths/partials/register_form.html", {"register_form": form})
                response['HX-Redirect'] = get_redirect_url_for_role(user)
                return response
    else:
        form = UserRegisterForm()
        
    return render(request, "userauths/partials/register_form.html", {"register_form": form})

def logout_view(request):
    logout(request)
    return redirect("core:home")

@login_required(login_url='/auth/')
def profile_view(request):
    return render(request, "userauths/profile.html")