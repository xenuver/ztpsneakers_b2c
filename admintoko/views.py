from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from orders.models import Order, WarrantyClaim, OrderItem
from products.models import Product, ProductSize, Review
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

def is_admin_toko(user):
    """
    Superuser punya akses penuh ke semua panel (admin & admintoko).
    Karyawan dengan grup AdminToko hanya bisa masuk admintoko.
    Staff biasa (is_staff=True tanpa grup) hanya bisa masuk /admin/ Django.
    """
    if user.is_superuser:
        return True
    return user.is_authenticated and user.groups.filter(name='AdminToko').exists()

def login_view(request):
    if request.user.is_authenticated and is_admin_toko(request.user):
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
                
        if user and is_admin_toko(user):
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('admintoko:dashboard')
        else:
            messages.error(request, "Akses ditolak. Kredensial tidak valid atau Anda tidak memiliki akses ke panel ini.")
            
    return render(request, 'admintoko/login.html')

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
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

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'admintoko/products.html', context)

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def product_create_view(request):
    from products.models import Category, Brand, ProductImage
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        condition = request.POST.get('condition', 'new')
        crossed_price = request.POST.get('crossed_price') or None
        is_featured = request.POST.get('is_featured') == 'on'
        
        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            brand_id=brand_id,
            category_id=category_id,
            condition=condition,
            crossed_price=crossed_price,
            is_featured=is_featured,
        )
        
        sizes = request.POST.getlist('sizes[]')
        stocks = request.POST.getlist('stocks[]')
        for size, stock in zip(sizes, stocks):
            if size.strip():
                stock_val = int(stock) if stock.isdigit() else 0
                ProductSize.objects.create(product=product, size=size.strip(), stock=stock_val)

        # Proses upload gambar
        images = request.FILES.getlist('images')
        for i, img in enumerate(images):
            ProductImage.objects.create(
                product=product,
                image=img,
                is_primary=(i == 0),
                order=i
            )
                
        messages.success(request, f"Produk {product.name} berhasil ditambahkan.")
        return redirect('admintoko:products')
        
    context = {
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'conditions': Product.CONDITION_CHOICES,
    }
    return render(request, 'admintoko/product_form.html', context)


@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    from products.models import Category, Brand, ProductImage
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.brand_id = request.POST.get('brand')
        product.category_id = request.POST.get('category')
        product.condition = request.POST.get('condition', 'new')
        product.crossed_price = request.POST.get('crossed_price') or None
        product.is_featured = request.POST.get('is_featured') == 'on'
        product.save()
        
        sizes = request.POST.getlist('sizes[]')
        stocks = request.POST.getlist('stocks[]')
        existing_sizes = {s.size: s for s in product.sizes.all()}
        new_sizes = set()
        
        for size, stock in zip(sizes, stocks):
            size = size.strip()
            if size:
                new_sizes.add(size)
                stock_val = int(stock) if stock.isdigit() else 0
                if size in existing_sizes:
                    ps = existing_sizes[size]
                    ps.stock = stock_val
                    ps.save()
                else:
                    ProductSize.objects.create(product=product, size=size, stock=stock_val)
                    
        for size_str, ps in existing_sizes.items():
            if size_str not in new_sizes:
                ps.stock = 0
                ps.save()

        # Hapus gambar yang dipilih
        delete_image_ids = request.POST.getlist('delete_images')
        if delete_image_ids:
            ProductImage.objects.filter(id__in=delete_image_ids, product=product).delete()

        # Proses upload gambar baru
        new_images = request.FILES.getlist('images')
        existing_count = product.images.count()
        has_primary = product.images.filter(is_primary=True).exists()
        for i, img in enumerate(new_images):
            is_primary = not has_primary and i == 0 and existing_count == 0
            ProductImage.objects.create(
                product=product,
                image=img,
                is_primary=is_primary,
                order=existing_count + i
            )

        # Pastikan selalu ada gambar primary
        if product.images.exists() and not product.images.filter(is_primary=True).exists():
            first_img = product.images.first()
            first_img.is_primary = True
            first_img.save()
                
        messages.success(request, f"Produk {product.name} berhasil diperbarui.")
        return redirect('admintoko:products')
        
    context = {
        'product': product,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'conditions': Product.CONDITION_CHOICES,
    }
    return render(request, 'admintoko/product_form.html', context)


@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
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

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def warranty_view(request):
    claims = WarrantyClaim.objects.all().order_by('-created_at')
    context = {
        'claims': claims
    }
    return render(request, 'admintoko/warranty.html', context)

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def reviews_view(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {
        'reviews': reviews
    }
    return render(request, 'admintoko/reviews.html', context)

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def product_toggle_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.is_active = not product.is_active
        product.save()
        messages.success(request, f"Status produk {product.name} berhasil diperbarui.")
    return redirect('admintoko:products')

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def order_update_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        tracking_number = request.POST.get('tracking_number')
        
        old_status = order.status
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        if tracking_number:
            order.tracking_number = tracking_number
        order.save()
        
        # Kirim email notifikasi sesuai status baru
        if new_status != old_status:
            from orders.email_utils import send_order_shipped_email, send_order_completed_email
            try:
                if new_status == 'shipped':
                    send_order_shipped_email(order)
                elif new_status == 'completed':
                    send_order_completed_email(order)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Email error for order {order.order_number}: {e}")
        
        messages.success(request, f"Pesanan #{order.order_number} berhasil diperbarui.")
    return redirect('admintoko:orders')


@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
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

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def review_toggle_view(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.is_visible = not getattr(review, 'is_visible', True)
        review.save()
        messages.success(request, f"Visibilitas ulasan berhasil diperbarui.")
    return redirect('admintoko:reviews')

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def customers_view(request):
    from userauths.models import User
    customers = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    context = {
        'customers': customers
    }
    return render(request, 'admintoko/customers.html', context)

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def category_create_view(request):
    if request.method == 'POST':
        from products.models import Category
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f"Kategori {name} berhasil ditambahkan.")
            return redirect('admintoko:products')
    return render(request, 'admintoko/category_form.html')

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def brand_create_view(request):
    if request.method == 'POST':
        from products.models import Brand
        name = request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            messages.success(request, f"Brand {name} berhasil ditambahkan.")
            return redirect('admintoko:products')
    return render(request, 'admintoko/brand_form.html')

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def categories_view(request):
    from products.models import Category
    categories = Category.objects.all().order_by('name')
    return render(request, 'admintoko/categories.html', {'categories': categories})

@user_passes_test(is_admin_toko, login_url='/admintoko/login/')
def brands_view(request):
    from products.models import Brand
    brands = Brand.objects.all().order_by('name')
    return render(request, 'admintoko/brands.html', {'brands': brands})
