from django.shortcuts import render, get_object_or_404, redirect
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
            request.session['cart_initialized'] = True
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart

def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        from django.urls import reverse
        request.session['pending_wishlist_item'] = product_id
        auth_url = reverse('userauths:auth_main')
        if request.META.get('HTTP_HX_REQUEST'):
            response = HttpResponse()
            response['HX-Redirect'] = auth_url
            return response
        return HttpResponse(f"""<script>window.location.href='{auth_url}';</script>""")
        
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
        if not request.user.is_authenticated:
            from django.urls import reverse
            request.session['pending_cart_item'] = {
                'product_id': product_id,
                'size_id': request.POST.get('size_choice'),
            }
            auth_url = reverse('userauths:auth_main')
            if request.META.get('HTTP_HX_REQUEST'):
                response = HttpResponse()
                response['HX-Redirect'] = auth_url
                return response
            return redirect('userauths:auth_main')
            
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
                if request.META.get('HTTP_HX_REQUEST'):
                    response = HttpResponse()
                    import json
                    response['HX-Trigger'] = json.dumps({"showToast": {"message": "Melebihi batas stok tersedia", "type": "error"}})
                    return response
                from django.contrib import messages
                messages.error(request, "Melebihi stok")
                return redirect('orders:cart_page')
                
        if request.META.get('HTTP_HX_REQUEST'):
            response = HttpResponse()
            import json
            response['HX-Trigger'] = json.dumps({
                "cartUpdated": True,
                "showToast": {"message": "Produk berhasil ditambahkan ke keranjang", "type": "success"}
            })
            return response
            
        return redirect('orders:cart_page')
        
    return HttpResponseForbidden()

def cart_drawer(request):
    cart = get_or_create_cart(request)
    response = render(request, "orders/partials/cart_drawer_content.html", {'cart': cart})
    response['HX-Trigger'] = 'openCart'
    return response

def cart_count(request):
    """HTMX endpoint: kembalikan badge count keranjang."""
    cart = get_or_create_cart(request)
    total_items = sum(item.quantity for item in cart.items.all())
    return render(request, "orders/partials/cart_count_badge.html", {'total_items': total_items})

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

from django.contrib.auth.decorators import login_required

@login_required
def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect('orders:cart_page')
        
    from .utils import generate_midtrans_snap_token
    
    if request.method == 'POST':
        shipping_service_raw = request.POST.get('shipping_service', '')
        shipping_service = ""
        from decimal import Decimal
        shipping_cost = Decimal('0')
        if shipping_service_raw:
            try:
                parts = shipping_service_raw.split('|')
                shipping_service = parts[0]
                shipping_cost = Decimal(parts[1])
            except:
                pass
                
        subtotal = cart.get_total_price()
        
        applied_voucher_data = request.session.get('applied_voucher', None)
        discount_amount = Decimal('0')
        voucher_obj = None
        
        if applied_voucher_data:
            from .models import Voucher
            try:
                voucher_obj = Voucher.objects.get(code=applied_voucher_data['code'])
                if voucher_obj.is_valid(subtotal):
                    discount_amount = Decimal(str(applied_voucher_data['discount_amount']))
            except Voucher.DoesNotExist:
                pass
                
        total = subtotal - discount_amount + shipping_cost
        
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
        # Extract courier from "JNE CTC"
        selected_courier = shipping_service.split(' ')[0] if shipping_service else "UNKNOWN"
        
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            status='pending',
            courier=selected_courier,
            shipping_service=shipping_service,
            shipping_cost=shipping_cost,
            voucher=voucher_obj,
            discount_amount=discount_amount,
            subtotal=subtotal,
            total=total
        )
        
        # Buat OrderItems dan kurangi stok (Booking Stock)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size_str=item.size.size,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            
            # Booking Stock: Kurangi stok langsung
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
            province_name=request.POST.get('province_name', 'Tidak Diketahui'),
            city_id=request.POST.get('city_id', ''),
            city_name=request.POST.get('city_name', 'Tidak Diketahui'),
            district_name=request.POST.get('district_name', ''),
            postal_code=request.POST.get('postal_code', ''),
            full_address=request.POST.get('full_address', '')
        )
        
        # Generate Snap Token
        snap_token = generate_midtrans_snap_token(order)
        if snap_token:
            order.midtrans_transaction_id = snap_token # We can store token here temporarily
            order.save()
            
        # Clear Cart and Voucher
        cart.items.all().delete()
        if 'applied_voucher' in request.session:
            del request.session['applied_voucher']
        
        # Tandai voucher sebagai sudah digunakan
        if voucher_obj and voucher_obj.user:
            voucher_obj.is_used = True
            voucher_obj.save()
        
        # Kirim email konfirmasi pesanan
        from .email_utils import send_order_confirmation_email
        send_order_confirmation_email(order)
        
        return redirect('orders:checkout_success', order_number=order.order_number)

    
    # Pass applied voucher to template
    applied_voucher = request.session.get('applied_voucher', None)
    
    from django.utils import timezone
    from django.db.models import Q
    from .models import Voucher
    now = timezone.now()
    available_vouchers = Voucher.objects.filter(
        is_active=True,
        is_used=False,
        valid_from__lte=now,
        valid_to__gte=now
    ).filter(
        Q(user__isnull=True) | Q(user=request.user)
    )
    
    context = {
        'cart': cart,
        'applied_voucher': applied_voucher,
        'available_vouchers': available_vouchers,
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

def get_provinces_options(request):
    from .utils import get_rajaongkir_provinces
    from django.urls import reverse
    provinces = get_rajaongkir_provinces()
    cities_url = reverse('orders:get_cities')
    html = f'''<select name="province_id" required 
                    hx-get="{cities_url}" 
                    hx-target="#city_select" 
                    class="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition">
                <option value="">Pilih Provinsi</option>'''
    for prov in provinces:
        html += f'<option value="{prov.get("id")}">{prov.get("name")}</option>'
    html += '</select>'
    return HttpResponse(html)

def get_cities(request):
    province_id = request.GET.get('province_id')
    if not province_id:
        return HttpResponse('<option value="">Pilih Kota</option>')
    
    from .utils import get_rajaongkir_cities
    cities = get_rajaongkir_cities(province_id)
    
    html = '<option value="">Pilih Kota</option>'
    for city in cities:
        html += f'<option value="{city.get("id")}">{city.get("name")}</option>'
    return HttpResponse(html)

def get_shipping_cost(request):
    province_id = request.GET.get('province_id')
    city_id = request.GET.get('city_id')
    
    if not city_id:
        return HttpResponse('<div class="text-center py-4 text-sm text-gray-400">Pilih kota terlebih dahulu.</div>')
        
    from .utils import calculate_shipping_cost
    origin_city = "152"  # Jakarta Pusat
    weight = 1000  # 1 kg
    
    couriers = ['jne', 'pos', 'tiki']
    all_costs_html = '<div class="space-y-3">'
    has_results = False
    opt_index = 0
    
    for courier in couriers:
        results = calculate_shipping_cost(origin_city, city_id, weight, courier)
        if results and len(results) > 0:
            has_results = True
            for cost in results:
                service = cost.get('service', '')
                price = cost.get('cost', 0)
                etd = cost.get('etd', '-')
                courier_code = cost.get('code', courier).upper()
                formatted_price = f'{price:,.0f}'.replace(',', '.')
                
                # Tambahkan nama kurir ke dalam value form
                service_value = f"{courier_code} {service}"
                
                all_costs_html += f'''
                <div class="shipping-option">
                    <input type="radio" name="shipping_service" value="{service_value}|{price}" 
                           id="ship_{opt_index}" class="sr-only peer" required>
                    <label for="ship_{opt_index}" class="shipping-label relative flex items-center justify-between 
                           border-2 border-gray-200 rounded-xl px-4 py-4 cursor-pointer 
                           hover:border-gray-400 transition-all peer-checked:border-primary 
                           peer-checked:bg-green-50 peer-checked:shadow-md">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                                <span class="text-xs font-extrabold text-gray-700">{courier_code}</span>
                            </div>
                            <div>
                                <p class="font-bold text-black text-sm uppercase tracking-wider">{courier_code} {service}</p>
                                <p class="text-gray-500 text-xs mt-0.5">Estimasi {etd} hari</p>
                            </div>
                        </div>
                        <div class="text-right flex items-center gap-3">
                            <p class="font-extrabold text-black">Rp {formatted_price}</p>
                            <div class="check-icon hidden w-6 h-6 rounded-full bg-primary text-white items-center justify-center flex-shrink-0">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                            </div>
                        </div>
                    </label>
                </div>'''
                opt_index += 1

    if not has_results:
        all_costs_html += '<div class="text-center py-4"><p class="text-red-500 text-sm font-semibold">Gagal mengambil data ongkos kirim.</p><p class="text-xs text-gray-400 mt-1">Pastikan koneksi API valid atau coba lagi.</p></div>'
        
    all_costs_html += '</div>'
    return HttpResponse(all_costs_html)

def update_total(request):
    cart = get_or_create_cart(request)
    shipping_service = request.POST.get('shipping_service')
    subtotal = cart.get_total_price()
    from decimal import Decimal
    shipping_cost = Decimal('0')
    if shipping_service:
        try:
            shipping_cost = Decimal(shipping_service.split('|')[1])
        except:
            pass
            
    applied_voucher_data = request.session.get('applied_voucher', None)
    discount_amount = Decimal('0')
    if applied_voucher_data:
        from .models import Voucher
        try:
            voucher_obj = Voucher.objects.get(code=applied_voucher_data['code'])
            if voucher_obj.is_valid(subtotal):
                discount_amount = Decimal(str(applied_voucher_data['discount_amount']))
        except Voucher.DoesNotExist:
            pass
            
    total = subtotal - discount_amount + shipping_cost
    
    html = f"""
    <div id="total-payment" class="border-t border-gray-100 pt-4 mb-6 flex justify-between items-center">
        <span class="text-base font-bold text-black uppercase tracking-wider">Total Pembayaran</span>
        <div class="text-right">
            <span class="text-xs text-gray-500 block mb-1">Subtotal + Ongkir (Rp {shipping_cost:,.0f})</span>
            """
    if discount_amount > 0:
        html += f'<span class="text-xs text-green-600 font-bold block mb-1">Diskon (Rp {discount_amount:,.0f})</span>'
            
    html += f"""
            <span class="text-2xl font-extrabold text-primary">Rp {total:,.0f}</span>
        </div>
    </div>
    """
    return HttpResponse(html)

@login_required
def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    from django.conf import settings
    
    # Midtrans client key for frontend Snap popup
    server_key = getattr(settings, 'MIDTRANS_SERVER_KEY', '')
    client_key = getattr(settings, 'MIDTRANS_CLIENT_KEY', '')
    is_production = getattr(settings, 'MIDTRANS_IS_PRODUCTION', False)
    
    context = {
        'order': order,
        'client_key': client_key,
        'midtrans_is_production': is_production,
    }
    return render(request, "orders/checkout_success.html", context)

from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
from django.conf import settings

@csrf_exempt
def midtrans_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            transaction_status = data.get('transaction_status')
            status_code = data.get('status_code')
            gross_amount = data.get('gross_amount')
            
            # Verifikasi signature
            server_key = getattr(settings, 'MIDTRANS_SERVER_KEY', '')
            signature_key = data.get('signature_key', '')
            raw_string = f"{order_id}{status_code}{gross_amount}{server_key}"
            computed_hash = hashlib.sha512(raw_string.encode()).hexdigest()
            
            if computed_hash != signature_key:
                return HttpResponse("Invalid signature", status=403)
            
            if order_id:
                order = Order.objects.filter(order_number=order_id).first()
                if order:
                    if transaction_status in ['capture', 'settlement']:
                        if order.status != 'paid':
                            order.status = 'paid'
                            order.save()
                    elif transaction_status in ['deny', 'cancel', 'expire']:
                        if order.status != 'cancelled':
                            order.status = 'cancelled'
                            order.save()
                            # Kembalikan stok yang sudah dibooking
                            for item in order.items.all():
                                from products.models import ProductSize
                                try:
                                    product_size = ProductSize.objects.get(product=item.product, size=item.size_str)
                                    product_size.stock += item.quantity
                                    product_size.save()
                                except ProductSize.DoesNotExist:
                                    pass
            return HttpResponse("OK")
        except Exception as e:
            print(f"Webhook error: {e}")
            return HttpResponse("Error", status=400)
    return HttpResponseForbidden()


@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Generate midtrans token if it's missing (e.g. API failed during checkout)
    if order.status == 'pending' and not order.midtrans_transaction_id:
        from .utils import generate_midtrans_snap_token
        snap_token = generate_midtrans_snap_token(order)
        if snap_token:
            order.midtrans_transaction_id = snap_token
            order.save()
        else:
            from django.contrib import messages
            messages.error(request, "Gagal menghubungkan ke Midtrans API. Kunci server (Server Key) di .env mungkin tidak valid atau unauthorized.")
            
    from django.conf import settings
    
    server_key = getattr(settings, 'MIDTRANS_SERVER_KEY', '')
    client_key = getattr(settings, 'MIDTRANS_CLIENT_KEY', '')
    is_production = getattr(settings, 'MIDTRANS_IS_PRODUCTION', False)
    
    context = {
        'order': order,
        'client_key': client_key,
        'midtrans_is_production': is_production,
    }
    return render(request, "orders/detail.html", context)

@login_required
def print_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/invoice.html", {'order': order})

@login_required
def send_invoice_email_view(request, order_number):
    """Kirim email invoice ke pembeli atas permintaan."""
    if request.method != 'POST':
        return HttpResponseForbidden()
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    from .email_utils import send_invoice_email
    from django.contrib import messages
    success = send_invoice_email(order)
    if success:
        messages.success(request, f"Invoice pesanan #{order.order_number} berhasil dikirim ke {order.user.email}.")
    else:
        messages.error(request, "Gagal mengirim email invoice. Pastikan konfigurasi email sudah benar.")
    return redirect('orders:order_detail', order_number=order_number)


@login_required
def complete_order(request, order_number):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        if order.status == 'shipped':
            order.status = 'completed'
            order.save()
            
            from orders.email_utils import send_order_completed_email
            try:
                send_order_completed_email(order)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Email error for order {order.order_number}: {e}")
            
            from django.contrib import messages
            messages.success(request, f"Pesanan {order.order_number} telah ditandai selesai.")
            
        return redirect('orders:order_detail', order_number=order.order_number)
    return HttpResponseForbidden()

from products.models import Review
from core.validators import validate_image_file
from django.core.exceptions import ValidationError

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
        images = [
            request.FILES.get('image'),
            request.FILES.get('image2'),
            request.FILES.get('image3')
        ]
        
        # Validasi file gambar
        from django.contrib import messages
        for img in images:
            if img:
                try:
                    validate_image_file(img)
                except ValidationError as e:
                    messages.error(request, str(e.message))
                    return render(request, "orders/review_form.html", {'item': order_item})
        
        Review.objects.create(
            product=order_item.product,
            user=request.user,
            order_item=order_item,
            rating=rating,
            comment=comment,
            image=images[0],
            image2=images[1],
            image3=images[2]
        )
        
        messages.success(request, "Ulasan berhasil dikirim. Terima kasih!")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    return render(request, "orders/review_form.html", {'item': order_item})

from .models import WarrantyClaim

@login_required
def create_warranty_claim(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    
    if order_item.order.status != 'completed':
        return HttpResponseForbidden("Klaim garansi hanya bisa dilakukan untuk pesanan yang sudah selesai.")
        
    from django.utils import timezone
    from datetime import timedelta
    if order_item.order.updated_at < timezone.now() - timedelta(days=7):
        from django.contrib import messages
        messages.error(request, "Batas waktu klaim garansi (7 hari sejak pesanan selesai) telah berakhir.")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    if order_item.has_warranty_claim:
        from django.contrib import messages
        messages.info(request, "Anda sudah mengajukan klaim garansi untuk produk ini.")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    if request.method == 'POST':
        kategori = request.POST.get('kategori', 'lainnya')
        reason = request.POST.get('reason')
        evidence_image = request.FILES.get('evidence_image')
        
        if evidence_image:
            from core.validators import validate_image_file
            from django.core.exceptions import ValidationError
            try:
                validate_image_file(evidence_image)
            except ValidationError as e:
                from django.contrib import messages
                messages.error(request, str(e.message))
                return render(request, "orders/warranty_form.html", {'item': order_item})
        
        claim = WarrantyClaim.objects.create(
            order_item=order_item,
            user=request.user,
            kategori=kategori,
            reason=reason,
            evidence_image=evidence_image
        )
        
        # Notifikasi dihapus dari view ini karena sudah ditangani oleh signal di orders/signals.py
        
        from django.contrib import messages
        messages.success(request, "Klaim garansi berhasil diajukan dan akan segera kami proses.")
        return redirect('orders:order_detail', order_number=order_item.order.order_number)
        
    return render(request, "orders/warranty_form.html", {'item': order_item})


@login_required
def warranty_tracking(request, claim_id):
    """Halaman tracking status klaim garansi."""
    claim = get_object_or_404(WarrantyClaim, id=claim_id, user=request.user)
    return render(request, "orders/warranty_tracking.html", {'claim': claim})


@login_required
def manual_check_payment_status(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    from .utils import check_midtrans_payment_status
    status_response = check_midtrans_payment_status(order)
    from django.contrib import messages
    
    if status_response:
        transaction_status = status_response.get('transaction_status')
        if transaction_status in ['capture', 'settlement']:
            order.status = 'paid'
            order.save()
            messages.success(request, f'Status pembayaran pesanan {order_number} berhasil diperbarui (Lunas).')
        elif transaction_status in ['pending']:
            messages.warning(request, f'Pembayaran pesanan {order_number} masih pending.')
        elif transaction_status in ['deny', 'cancel', 'expire']:
            if order.status != 'cancelled':
                order.status = 'cancelled'
                order.save()
                
                # Kembalikan stok yang sudah dibooking
                for item in order.items.all():
                    from products.models import ProductSize
                    try:
                        product_size = ProductSize.objects.get(product=item.product, size=item.size_str)
                        product_size.stock += item.quantity
                        product_size.save()
                    except ProductSize.DoesNotExist:
                        pass
                        
            messages.error(request, f'Pembayaran pesanan {order_number} gagal/dibatalkan.')
        else:
            messages.info(request, f'Status transaksi: {transaction_status}')
    else:
        messages.error(request, 'Gagal mengecek status ke Midtrans. Pastikan pesanan sudah dibuat di Midtrans (token valid).')
        
    return redirect('orders:order_detail', order_number=order_number)

@login_required
def apply_voucher(request):
    if request.method == 'POST':
        code = request.POST.get('voucher_code', '').strip()
        cart = request.user.cart if hasattr(request.user, 'cart') else None
        
        if not cart or cart.items.count() == 0:
            return HttpResponse('<div class="text-red-500 text-sm mt-1">Keranjang kosong.</div>')
            
        subtotal = cart.get_total_price()
        
        from .models import Voucher
        try:
            voucher = Voucher.objects.get(code__iexact=code)
            if voucher.is_valid(subtotal):
                discount = voucher.calculate_discount(subtotal)
                # Simpan voucher ke sesi agar bisa dipakai saat checkout
                request.session['applied_voucher'] = {
                    'code': voucher.code,
                    'discount_amount': float(discount)
                }
                return HttpResponse(f'<div class="text-green-600 text-sm mt-1 font-bold">Voucher berhasil diterapkan! Diskon Rp {discount:,.0f}</div><script>setTimeout(() => window.location.reload(), 1000);</script>')
            else:
                return HttpResponse('<div class="text-red-500 text-sm mt-1">Voucher tidak valid atau syarat pembelian belum terpenuhi.</div>')
        except Voucher.DoesNotExist:
            return HttpResponse('<div class="text-red-500 text-sm mt-1">Kode voucher tidak ditemukan.</div>')
            
    return HttpResponse('')
