from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from orders.models import Order, WarrantyClaim, OrderItem
from products.models import Product, ProductSize, Review
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def is_admin_toko(user):
    return user.is_authenticated and user.groups.filter(name='AdminToko').exists()

def login_view(request):
    if request.user.is_authenticated and request.user.groups.filter(name='AdminToko').exists():
        return redirect('admintoko:dashboard')
        
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        email = request.POST.get('email')
        password = request.POST.get('password')
        # user model uses email for auth via identifier logic, but authenticate needs correct kwargs
        # since we have custom auth backend handling identifier, we can use that or simple username
        user = authenticate(request, username=email, password=password)
        if not user:
            # fallback if authenticate doesn't handle email properly in custom setup
            from userauths.models import User
            user_obj = User.objects.filter(email=email).first()
            if user_obj and user_obj.check_password(password):
                user = user_obj
                
        if user and user.groups.filter(name='AdminToko').exists():
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('admintoko:dashboard')
        else:
            messages.error(request, "Akses ditolak. Kredensial tidak valid atau Anda bukan Admin Toko.")
            
    return render(request, 'admintoko/login.html')

@user_passes_test(is_admin_toko, login_url='/auth/')
def dashboard_view(request):
    today = timezone.now().date()
    
    # Ringkasan Pesanan Hari Ini
    orders_today = Order.objects.filter(created_at__date=today)
    pending_orders = orders_today.filter(status='pending').count()
    paid_orders = orders_today.filter(status='paid').count()
    
    # Laporan Garansi Baru
    new_warranty_claims = WarrantyClaim.objects.filter(status='pending').count()
    
    # Stok Menipis (<= 2)
    low_stock_sizes = ProductSize.objects.filter(stock__lte=2, product__is_active=True).select_related('product')
    
    context = {
        'orders_today_count': orders_today.count(),
        'pending_orders': pending_orders,
        'paid_orders': paid_orders,
        'new_warranty_claims': new_warranty_claims,
        'low_stock_sizes': low_stock_sizes,
    }
    return render(request, 'admintoko/dashboard.html', context)

@user_passes_test(is_admin_toko, login_url='/admin-toko/login/')
def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'admintoko/products.html', context)

@user_passes_test(is_admin_toko, login_url='/admin-toko/login/')
def product_create_view(request):
    from products.models import Category, Brand
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        
        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            brand_id=brand_id,
            category_id=category_id
        )
        messages.success(request, f"Produk {product.name} berhasil ditambahkan.")
        return redirect('admintoko:products')
        
    context = {
        'brands': Brand.objects.all(),
        'categories': Category.objects.all()
    }
    return render(request, 'admintoko/product_form.html', context)

@user_passes_test(is_admin_toko, login_url='/admin-toko/login/')
def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    from products.models import Category, Brand
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.brand_id = request.POST.get('brand')
        product.category_id = request.POST.get('category')
        product.save()
        messages.success(request, f"Produk {product.name} berhasil diperbarui.")
        return redirect('admintoko:products')
        
    context = {
        'product': product,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all()
    }
    return render(request, 'admintoko/product_form.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def orders_view(request):
    status_filter = request.GET.get('status', 'all')
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
        
    context = {
        'orders': orders,
        'current_status': status_filter
    }
    return render(request, 'admintoko/orders.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def warranty_view(request):
    claims = WarrantyClaim.objects.all().order_by('-created_at')
    context = {
        'claims': claims
    }
    return render(request, 'admintoko/warranty.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def reviews_view(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {
        'reviews': reviews
    }
    return render(request, 'admintoko/reviews.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def product_toggle_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.is_active = not product.is_active
        product.save()
        messages.success(request, f"Status produk {product.name} berhasil diperbarui.")
    return redirect('admintoko:products')

@user_passes_test(is_admin_toko, login_url='/auth/')
def order_update_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        tracking_number = request.POST.get('tracking_number')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        if tracking_number:
            order.tracking_number = tracking_number
        order.save()
        messages.success(request, f"Pesanan #{order.order_number} berhasil diperbarui.")
    return redirect('admintoko:orders')

@user_passes_test(is_admin_toko, login_url='/auth/')
def warranty_update_status(request, claim_id):
    if request.method == 'POST':
        claim = get_object_or_404(WarrantyClaim, id=claim_id)
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes')
        
        if new_status in dict(WarrantyClaim.STATUS_CHOICES):
            claim.status = new_status
        if admin_notes is not None:
            claim.admin_notes = admin_notes
        claim.save()
        messages.success(request, f"Klaim garansi #{claim.id} berhasil diperbarui.")
    return redirect('admintoko:warranty')

@user_passes_test(is_admin_toko, login_url='/auth/')
def review_toggle_view(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.is_visible = not getattr(review, 'is_visible', True)
        review.save()
        messages.success(request, f"Visibilitas ulasan berhasil diperbarui.")
    return redirect('admintoko:reviews')

@user_passes_test(is_admin_toko, login_url='/auth/')
def customers_view(request):
    from userauths.models import User
    customers = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    context = {
        'customers': customers
    }
    return render(request, 'admintoko/customers.html', context)

