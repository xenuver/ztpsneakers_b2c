from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from orders.models import Order, WarrantyClaim, OrderItem
from products.models import Product, ProductSize, Review
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def is_admin_toko(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

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
    return render(request, 'admin_toko/dashboard.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'admin_toko/products.html', context)

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
    return render(request, 'admin_toko/orders.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def warranty_view(request):
    claims = WarrantyClaim.objects.all().order_by('-created_at')
    context = {
        'claims': claims
    }
    return render(request, 'admin_toko/warranty.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def reviews_view(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {
        'reviews': reviews
    }
    return render(request, 'admin_toko/reviews.html', context)

@user_passes_test(is_admin_toko, login_url='/auth/')
def product_toggle_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.is_active = not product.is_active
        product.save()
        messages.success(request, f"Status produk {product.name} berhasil diperbarui.")
    return redirect('admin_toko:products')

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
    return redirect('admin_toko:orders')

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
    return redirect('admin_toko:warranty')

@user_passes_test(is_admin_toko, login_url='/auth/')
def review_toggle_view(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.is_visible = not getattr(review, 'is_visible', True)
        review.save()
        messages.success(request, f"Visibilitas ulasan berhasil diperbarui.")
    return redirect('admin_toko:reviews')

@user_passes_test(is_admin_toko, login_url='/auth/')
def customers_view(request):
    from userauths.models import User
    customers = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    context = {
        'customers': customers
    }
    return render(request, 'admin_toko/customers.html', context)

