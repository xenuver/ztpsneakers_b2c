from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db.models import Q
from .models import User

def auth_main(request):
    if request.user.is_authenticated:
        return redirect("storefront:home")
    return render(request, "userauths/auth_base.html")

def auth_check(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        if not identifier:
            response = HttpResponse('<div class="text-red-500 font-bold mb-4 text-center text-sm">Silakan masukkan email atau nomor HP yang valid</div>')
            response['HX-Retarget'] = '#auth-error'
            return response
            
        if identifier.isdigit() and len(identifier) < 12:
            response = HttpResponse('<div class="text-red-500 font-bold mb-4 text-center text-sm">Nomor HP harus minimal 12 digit</div>')
            response['HX-Retarget'] = '#auth-error'
            return response
            
        user = User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()
        
        if user:
            # Pindah ke input password
            return render(request, "userauths/partials/login_password.html", {"identifier": identifier})
        else:
            # Pindah ke input detail pendaftaran
            return render(request, "userauths/partials/register_details.html", {"identifier": identifier})
            
    return HttpResponse("Method not allowed", status=405)

def auth_login(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        
        user = User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()
        if user and user.check_password(password):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse("""<script>window.location.href='/';</script>""")
        else:
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Password salah</div>""", status=400)
            
    return HttpResponse("Method not allowed", status=405)

def auth_register(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        name = request.POST.get("name")
        
        # Cek apakah identifier adalah email atau hp (sederhana)
        is_email = '@' in identifier
        
        if User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).exists():
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Email/No HP sudah terdaftar</div>""", status=400)
            
        user = User.objects.create_user(
            username=identifier.split('@')[0] if is_email else identifier,
            email=identifier if is_email else f"{identifier}@placeholder.com",
            password=password,
            phone_number=identifier if not is_email else ""
        )
        # Boleh tambahkan logic first_name/last_name = name
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse("""<script>window.location.href='/';</script>""")
        
    return HttpResponse("Method not allowed", status=405)

def auth_logout(request):
    logout(request)
    return redirect("userauths:auth_main")

def auth_profile(request):
    if not request.user.is_authenticated:
        return redirect("userauths:auth_main")
        
    if request.method == "POST":
        request.user.username = request.POST.get("username", request.user.username)
        request.user.phone_number = request.POST.get("phone_number", request.user.phone_number)
        request.user.address = request.POST.get("address", request.user.address)
        request.user.save()
        return redirect("userauths:profile")
        
    return render(request, "userauths/profile.html")