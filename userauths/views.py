from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Import ketiga form yang ada di forms.py
from .forms import UserRegisterForm, UserEntryForm, UserLoginForm 

# 1. HALAMAN ENTRY
def entry_view(request):
    if request.method == "POST":
        form = UserEntryForm(request.POST)
        if form.is_valid():
            # Mengambil data yang sudah dibersihkan dari form
            identifier = form.cleaned_data.get("identifier")
            
            user_exists = User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).exists()
            request.session['auth_identifier'] = identifier
            
            if user_exists:
                return redirect("userauths:login")
            else:
                return redirect("userauths:register")
    else:
        form = UserEntryForm()
        
    return render(request, "userauths/entry.html", {"form": form})

# 2. HALAMAN LOGIN
def login_view(request):
    identifier = request.session.get('auth_identifier')
    
    if not identifier:
        return redirect("userauths:entry")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            
            user_obj = User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()
            
            if user_obj:
                user = authenticate(request, email=user_obj.email, password=password)
                if user is not None:
                    login(request, user)
                    if 'auth_identifier' in request.session:
                        del request.session['auth_identifier']
                    messages.success(request, f"Selamat datang kembali, {user.username}!")
                    return redirect("/")
                else:
                    messages.error(request, "Kata sandi salah!")
            else:
                messages.error(request, "Akun tidak ditemukan.")
    else:
        form = UserLoginForm()
        
    context = {
        'form': form,
        'identifier': identifier
    }
    return render(request, "userauths/login.html", context)

def register_view(request):
    identifier = request.session.get('auth_identifier')
    
    if not identifier:
        return redirect("userauths:entry")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # Simpan user baru
            login(request, user) # Langsung login
            del request.session['auth_identifier']
            messages.success(request, "Registrasi berhasil!")
            return redirect("core:home")
        else:
            # Jika ada error (misal password kurang kuat atau email sudah ada)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        # UX: Mengisi otomatis field email atau no HP dari halaman Entry
        initial_data = {}
        if '@' in identifier:
            initial_data['email'] = identifier
        else:
            initial_data['phone_number'] = identifier
            
        form = UserRegisterForm(initial=initial_data)

    context = {
        'form': form,
        'identifier': identifier
    }
    return render(request, "userauths/register.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Anda telah berhasil keluar.")
    return redirect("core:home")

@login_required(login_url='userauths:login')
def profile_view(request):
    # Sementara merender halaman kosong atau tulisan "Ini halaman profil"
    # Nanti kamu bisa buat file profile.html di folder templates/userauths/
    return render(request, "userauths/profile.html")