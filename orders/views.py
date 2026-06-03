from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from products.models import Product, ProductSize
from .models import Wishlist, Cart, CartItem

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart

def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponse("""<script>window.location.href='/auth/';</script>""")
        
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wishlist.delete()
        is_wished = False
    else:
        is_wished = True
        
    if request.GET.get('from_wishlist') and not is_wished:
        return HttpResponse("")
        
    # Kembalikan ikon heart via HTMX
    svg_fill = "currentColor" if is_wished else "none"
    text_color = "text-red-500" if is_wished else "text-gray-400"
    
    html = f"""
    <svg class="w-6 h-6 flex-shrink-0 {text_color}" fill="{svg_fill}" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
    </svg>
    <span class="sr-only">Toggle Wishlist</span>
    """
    return HttpResponse(html)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        size_id = request.POST.get('size_choice')
        
        if not size_id:
            # Mengembalikan response error form atau trigger event js
            return HttpResponse("Pilih ukuran terlebih dahulu", status=400)
            
        size = get_object_or_404(ProductSize, id=size_id, product=product)
        if size.stock <= 0:
            return HttpResponse("Stok habis", status=400)
            
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            size=size
        )
        
        if not created:
            if cart_item.quantity < size.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                return HttpResponse("Melebihi stok", status=400)
                
        # Trigger event HTMX untuk open cart drawer & update cart count
        response = render(request, "orders/partials/cart_drawer_content.html", {'cart': cart})
        response['HX-Trigger'] = 'openCart, cartUpdated'
        return response
        
    return HttpResponseForbidden()

def cart_drawer(request):
    cart = get_or_create_cart(request)
    return render(request, "orders/partials/cart_drawer_content.html", {'cart': cart})

def update_cart_item(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if action == 'increase':
            if item.quantity < item.size.stock:
                item.quantity += 1
                item.save()
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                
        # Return empty response but trigger events to reload cart components
        response = HttpResponse()
        response['HX-Trigger'] = 'cartUpdated'
        return response
    return HttpResponseForbidden()

def remove_cart_item(request, item_id):
    if request.method in ['POST', 'DELETE']:
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        response = HttpResponse()
        response['HX-Trigger'] = 'cartUpdated'
        return response
    return HttpResponseForbidden()

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, "orders/cart.html", {'cart': cart})

from django.utils.crypto import get_random_string
from .models import Order, OrderItem, ShippingAddress

def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return HttpResponse("""<script>window.location.href='/';</script>""")
        
    from .utils import get_rajaongkir_provinces, generate_midtrans_snap_token
    provinces = get_rajaongkir_provinces()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Harusnya dicegah dari awal atau diarahkan ke login, tapi ini fallback
            return redirect('userauths:auth_main')
            
        shipping_service_raw = request.POST.get('shipping_service', '')
        shipping_service = ""
        shipping_cost = 0
        if shipping_service_raw:
            try:
                parts = shipping_service_raw.split('|')
                shipping_service = parts[0]
                shipping_cost = float(parts[1])
            except:
                pass
                
        subtotal = cart.get_total_price()
        total = subtotal + shipping_cost
        
        # Validasi stok
        for item in cart.items.all():
            if item.size.stock < item.quantity:
                # Stock insufficient, redirect back to cart with error or handle gracefully
                # For now, let's just return HttpResponse error. Ideally we use messages framework
                from django.contrib import messages
                messages.error(request, f"Stok untuk {item.product.name} (Size: {item.size.size}) tidak mencukupi. Tersisa {item.size.stock}.")
                return redirect('orders:cart_page')
        
        # Buat Order
        order_number = f"ZTP-{get_random_string(10).upper()}"
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            status='pending',
            courier='jne', # Defaulting to JNE for now
            shipping_service=shipping_service,
            shipping_cost=shipping_cost,
            subtotal=subtotal,
            total=total
        )
        
        # Buat OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size_str=item.size.size,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            # Kurangi stok
            if item.size.stock >= item.quantity:
                item.size.stock -= item.quantity
                item.size.save()
        
        # Buat ShippingAddress
        # For city_name and province_name we'd ideally fetch them from the API or select text,
        # but for simplicity we'll just save the IDs for now
        ShippingAddress.objects.create(
            order=order,
            recipient_name=request.POST.get('recipient_name', ''),
            phone_number=request.POST.get('phone_number', ''),
            province_id=request.POST.get('province_id', ''),
            province_name='Provinsi',
            city_id=request.POST.get('city_id', ''),
            city_name='Kota',
            district_name=request.POST.get('district_name', ''),
            postal_code=request.POST.get('postal_code', ''),
            full_address=request.POST.get('full_address', '')
        )
        
        # Generate Snap Token
        snap_token = generate_midtrans_snap_token(order)
        if snap_token:
            order.midtrans_transaction_id = snap_token # We can store token here temporarily
            order.save()
            
        # Clear Cart
        cart.items.all().delete()
        
        return redirect('orders:checkout_success', order_number=order.order_number)
    
    context = {
        'cart': cart,
        'provinces': provinces,
    }
    return render(request, "orders/checkout.html", context)

from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    wishlists = request.user.wishlists.all()
    context = {
        'wishlists': wishlists,
    }
    return render(request, "orders/wishlist.html", context)

def get_cities(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return HttpResponse('<option value="">Pilih Kota</option>')
    
    from .utils import get_rajaongkir_cities
    cities = get_rajaongkir_cities(province_id)
    
    html = '<option value="">Pilih Kota</option>'
    for city in cities:
        html += f'<option value="{city.get("city_id")}">{city.get("type")} {city.get("city_name")}</option>'
    return HttpResponse(html)

def get_shipping_cost(request):
    province_id = request.GET.get('province_id')
    city_id = request.GET.get('city_id')
    
    if not city_id:
        return HttpResponse('')
        
    from .utils import calculate_shipping_cost
    # Asumsi origin Jakarta Pusat (ID: 152), berat 1000 gram (1kg)
    origin_city = "152"
    weight = 1000
    courier = "jne" # default courier
    
    results = calculate_shipping_cost(origin_city, city_id, weight, courier)
    
    html = ""
    if results and len(results) > 0:
        costs = results[0].get('costs', [])
        for cost in costs:
            service = cost.get('service')
            price = cost.get('cost', [{}])[0].get('value', 0)
            etd = cost.get('cost', [{}])[0].get('etd', '')
            html += f"""
            <label class="relative block bg-white border border-gray-200 rounded-lg shadow-sm px-4 py-4 cursor-pointer sm:flex sm:justify-between hover:border-gray-300">
                <input type="radio" name="shipping_service" value="{service}|{price}" class="sr-only" required hx-post="/pesanan/api/update-total/" hx-target="#total-payment">
                <div class="flex items-center">
                    <div class="text-sm">
                        <p class="font-bold text-black uppercase tracking-wider">{results[0].get('code')} - {service}</p>
                        <p class="text-gray-500 text-xs">Estimasi: {etd} hari</p>
                    </div>
                </div>
                <div class="mt-2 sm:mt-0 sm:block text-right">
                    <p class="font-bold text-black">Rp {price}</p>
                </div>
            </label>
            """
    else:
        html = '<p class="text-red-500 text-sm">Gagal mengambil data ongkos kirim. Pastikan API Key valid.</p>'
        
    return HttpResponse(html)

def update_total(request):
    cart = get_or_create_cart(request)
    shipping_service = request.POST.get('shipping_service')
    subtotal = cart.get_total_price()
    shipping_cost = 0
    if shipping_service:
        try:
            shipping_cost = float(shipping_service.split('|')[1])
        except:
            pass
            
    total = subtotal + shipping_cost
    
    html = f"""
    <div id="total-payment" class="border-t border-gray-100 pt-4 mb-6 flex justify-between items-center">
        <span class="text-base font-bold text-black uppercase tracking-wider">Total Pembayaran</span>
        <div class="text-right">
            <span class="text-xs text-gray-500 block mb-1">Subtotal + Ongkir (Rp {shipping_cost:,.0f})</span>
            <span class="text-2xl font-extrabold text-primary">Rp {total:,.0f}</span>
        </div>
    </div>
    """
    return HttpResponse(html)

@login_required
def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Midtrans client key for frontend Snap popup
    client_key = getattr(settings, 'MIDTRANS_CLIENT_KEY', '')
    
    context = {
        'order': order,
        'client_key': client_key,
    }
    return render(request, "orders/checkout_success.html", context)

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def midtrans_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            transaction_status = data.get('transaction_status')
            
            if order_id:
                order = Order.objects.filter(order_number=order_id).first()
                if order:
                    if transaction_status in ['capture', 'settlement']:
                        order.status = 'paid'
                    elif transaction_status in ['deny', 'cancel', 'expire']:
                        order.status = 'cancelled'
                    order.save()
            return HttpResponse("OK")
        except Exception as e:
            print(f"Webhook error: {e}")
            return HttpResponse("Error", status=400)
    return HttpResponseForbidden()

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders/history.html", {'orders': orders})

@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/detail.html", {'order': order})

@login_required
def print_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/invoice.html", {'order': order})

@login_required
def complete_order(request, order_number):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        if order.status == 'shipped':
            order.status = 'completed'
            order.save()
            
            from django.contrib import messages
            messages.success(request, f"Pesanan {order.order_number} telah ditandai selesai.")
            
        return redirect('orders:order_detail', order_number=order.order_number)
    return HttpResponseForbidden()

from products.models import Review

@login_required
def create_review(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    
    if order_item.order.status != 'completed':
        return HttpResponseForbidden("Anda hanya dapat memberikan ulasan untuk pesanan yang telah selesai.")
        
    if order_item.has_review:
        from django.contrib import messages
        messages.info(request, "Anda sudah memberikan ulasan untuk produk ini.")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        image = request.FILES.get('image')
        
        Review.objects.create(
            product=order_item.product,
            user=request.user,
            order_item=order_item,
            rating=rating,
            comment=comment,
            image=image
        )
        
        from django.contrib import messages
        messages.success(request, "Ulasan berhasil dikirim. Terima kasih!")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    return render(request, "orders/review_form.html", {'item': order_item})

from .models import WarrantyClaim

@login_required
def create_warranty_claim(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    
    if order_item.order.status != 'completed':
        return HttpResponseForbidden("Klaim garansi hanya bisa dilakukan untuk pesanan yang sudah selesai.")
        
    if order_item.has_warranty_claim:
        from django.contrib import messages
        messages.info(request, "Anda sudah mengajukan klaim garansi untuk produk ini.")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    if request.method == 'POST':
        reason = request.POST.get('reason')
        evidence_image = request.FILES.get('evidence_image')
        
        WarrantyClaim.objects.create(
            order_item=order_item,
            user=request.user,
            reason=reason,
            evidence_image=evidence_image
        )
        
        from django.contrib import messages
        messages.success(request, "Klaim garansi berhasil diajukan dan akan segera kami proses.")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    return render(request, "orders/warranty_form.html", {'item': order_item})
