from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db.models import Q
from .models import User

def auth_main(request):
    if request.user.is_authenticated:
        return redirect("storefront:home")
    
    active_tab = request.GET.get('tab', 'login')
    if request.headers.get('HX-Request'):
        if active_tab == 'login':
            return render(request, "userauths/partials/login_form.html")
        else:
            return render(request, "userauths/partials/register_form.html")
            
    return render(request, "userauths/auth_main.html", {'active_tab': active_tab})

def auth_check(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        if not identifier:
            response = HttpResponse('<div class="text-red-500 font-bold mb-4 text-center text-sm">Silakan masukkan email atau nomor HP yang valid</div>')
            response['HX-Retarget'] = '#auth-error'
            return response
            
        if identifier.isdigit() and len(identifier) < 10:
            response = HttpResponse('<div class="text-red-500 font-bold mb-4 text-center text-sm">Nomor HP harus minimal 10 digit</div>')
            response['HX-Retarget'] = '#auth-error'
            return response
            
        user = User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()
        
        if user:
            # Pindah ke input password
            return render(request, "userauths/partials/login_password.html", {"identifier": identifier})
        else:
            # Pindah ke input detail pendaftaran
            is_email = '@' in identifier
            context = {
                "email": identifier if is_email else "",
                "phone_number": identifier if not is_email else ""
            }
            return render(request, "userauths/partials/register_details.html", context)
            
    return HttpResponse("Method not allowed", status=405)

def auth_login(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")
        
        user = User.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()
        if user and user.check_password(password):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            from orders.utils import merge_guest_cart
            merge_guest_cart(request, user)
            
            pending_cart = request.session.pop('pending_cart_item', None)
            if pending_cart:
                from orders.models import Cart, CartItem
                from products.models import Product, ProductSize
                try:
                    product = Product.objects.get(id=pending_cart['product_id'])
                    size = ProductSize.objects.get(id=pending_cart['size_id'], product=product)
                    cart, _ = Cart.objects.get_or_create(user=user)
                    CartItem.objects.get_or_create(cart=cart, product=product, size=size)
                except (Product.DoesNotExist, ProductSize.DoesNotExist):
                    pass
            
            pending_wishlist = request.session.pop('pending_wishlist_item', None)
            if pending_wishlist:
                from orders.models import Wishlist
                from products.models import Product
                try:
                    product = Product.objects.get(id=pending_wishlist)
                    Wishlist.objects.get_or_create(user=user, product=product)
                except Product.DoesNotExist:
                    pass
            
            response = HttpResponse("Berhasil masuk")
            response['HX-Redirect'] = '/'
            return response
        else:
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Password salah</div>""")
            
    return HttpResponse("Method not allowed", status=405)

def auth_register(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        name = request.POST.get("name")
        
        if password != password_confirm:
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Password tidak cocok</div>""")
        
        if not email or not phone_number:
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Email dan Nomor HP wajib diisi</div>""")
            
        if phone_number.isdigit() and len(phone_number) < 10:
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Nomor HP harus minimal 10 digit</div>""")
            
        if User.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists():
            return HttpResponse("""<div class="text-red-500 text-sm mt-2">Email/No HP sudah terdaftar</div>""")
            
        user = User.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password=password,
            phone_number=phone_number,
            first_name=name
        )
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        from orders.models import Voucher
        from django.utils import timezone
        from datetime import timedelta
        import uuid
        voucher_code = f"WELCOME-{uuid.uuid4().hex[:8].upper()}"
        Voucher.objects.create(
            code=voucher_code,
            discount_type='percentage',
            discount_value=10,
            min_purchase=0,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=30),
            is_active=True,
            user=user,
        )
        
        from orders.utils import merge_guest_cart
        merge_guest_cart(request, user)
        
        pending_cart = request.session.pop('pending_cart_item', None)
        if pending_cart:
            from orders.models import Cart, CartItem
            from products.models import Product, ProductSize
            try:
                product = Product.objects.get(id=pending_cart['product_id'])
                size = ProductSize.objects.get(id=pending_cart['size_id'], product=product)
                cart, _ = Cart.objects.get_or_create(user=user)
                CartItem.objects.get_or_create(cart=cart, product=product, size=size)
            except (Product.DoesNotExist, ProductSize.DoesNotExist):
                pass
        
        pending_wishlist = request.session.pop('pending_wishlist_item', None)
        if pending_wishlist:
            from orders.models import Wishlist
            from products.models import Product
            try:
                product = Product.objects.get(id=pending_wishlist)
                Wishlist.objects.get_or_create(user=user, product=product)
            except Product.DoesNotExist:
                pass
        
        response = HttpResponse("Berhasil daftar")
        response['HX-Redirect'] = '/'
        return response
        
    return HttpResponse("Method not allowed", status=405)

def auth_logout(request):
    logout(request)
    return redirect("/")

def auth_profile(request):
    if not request.user.is_authenticated:
        return redirect("userauths:auth_main")
        
    if request.method == "POST":
        request.user.username = request.POST.get("username", request.user.username)
        request.user.phone_number = request.POST.get("phone_number", request.user.phone_number)
        request.user.address = request.POST.get("address", request.user.address)
        
        avatar = request.FILES.get("avatar")
        if avatar:
            request.user.avatar = avatar
            
        request.user.save()
        return redirect("userauths:profile")
        
    from orders.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'recent_orders': orders
    }
    return render(request, "userauths/profile.html", context)