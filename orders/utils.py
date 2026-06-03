from django.core.cache import cache
import requests
from django.conf import settings
import midtransclient

def get_rajaongkir_provinces():
    cached_provinces = cache.get('rajaongkir_provinces')
    if cached_provinces is not None:
        return cached_provinces
        
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', '')
    url = "https://rajaongkir.komerce.id/api/v1/destination/province"
    headers = {"key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json().get('data', [])
            cache.set('rajaongkir_provinces', results, 60 * 60 * 24) # 24 hours
            return results
    except Exception as e:
        print(f"RajaOngkir (Komerce) error: {e}")
        
    # Fallback if API fails (e.g. timeout)
    fallback_provinces = [
        {"id": 10, "name": "DKI JAKARTA"},
        {"id": 5, "name": "JAWA BARAT"},
        {"id": 12, "name": "JAWA TENGAH"},
        {"id": 18, "name": "JAWA TIMUR"},
        {"id": 19, "name": "DI YOGYAKARTA"},
        {"id": 11, "name": "BANTEN"},
    ]
    return fallback_provinces

def get_rajaongkir_cities(province_id):
    cache_key = f'rajaongkir_cities_{province_id}'
    cached_cities = cache.get(cache_key)
    if cached_cities is not None:
        return cached_cities
        
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', '')
    url = f"https://rajaongkir.komerce.id/api/v1/destination/city/{province_id}"
    headers = {"key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json().get('data', [])
            cache.set(cache_key, results, 60 * 60 * 24)
            return results
    except Exception as e:
        print(f"RajaOngkir (Komerce) error: {e}")
        
    # Fallback if API fails
    fallback_cities = [
        {"id": 135, "province_id": 10, "name": "JAKARTA BARAT"},
        {"id": 137, "province_id": 10, "name": "JAKARTA PUSAT"},
        {"id": 136, "province_id": 10, "name": "JAKARTA SELATAN"},
        {"id": 139, "province_id": 10, "name": "JAKARTA TIMUR"},
        {"id": 138, "province_id": 10, "name": "JAKARTA UTARA"},
        {"id": 22, "province_id": 5, "name": "BANDUNG"},
        {"id": 115, "province_id": 5, "name": "DEPOK"},
        {"id": 54, "province_id": 5, "name": "BEKASI"},
        {"id": 39, "province_id": 12, "name": "SEMARANG"},
        {"id": 444, "province_id": 18, "name": "SURABAYA"},
        {"id": 501, "province_id": 19, "name": "YOGYAKARTA"},
        {"id": 451, "province_id": 11, "name": "TANGERANG"},
    ]
    # Filter fallback by requested province
    filtered_fallback = [c for c in fallback_cities if str(c.get('province_id', '')) == str(province_id)]
    return filtered_fallback if filtered_fallback else fallback_cities

def calculate_shipping_cost(origin_city, destination_city, weight, courier):
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', '')
    url = "https://rajaongkir.komerce.id/api/v1/calculate/domestic-cost"
    headers = {"key": api_key, "content-type": "application/x-www-form-urlencoded"}
    payload = f"origin={origin_city}&destination={destination_city}&weight={weight}&courier={courier}"
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            # Return directly as it's already a list of services in Komerce API
            return response.json().get('data', [])
    except Exception as e:
        print(f"RajaOngkir (Komerce) error: {e}")
        
    # Return None jika API gagal, jangan pakai fallback dummy
    return None

def generate_midtrans_snap_token(order):
    server_key = getattr(settings, 'MIDTRANS_SERVER_KEY', '')
    client_key = getattr(settings, 'MIDTRANS_CLIENT_KEY', '')
    is_production = getattr(settings, 'MIDTRANS_IS_PRODUCTION', False)
    
    snap = midtransclient.Snap(
        is_production=is_production,
        server_key=server_key,
        client_key=client_key
    )
    
    param = {
        "transaction_details": {
            "order_id": order.order_number,
            "gross_amount": int(order.total)
        },
        "customer_details": {
            "first_name": order.shipping_address.recipient_name if hasattr(order, 'shipping_address') else "Customer",
            "email": order.user.email if order.user else "guest@example.com",
            "phone": order.shipping_address.phone_number if hasattr(order, 'shipping_address') else ""
        }
    }
    
    try:
        transaction = snap.create_transaction(param)
        return transaction['token']
    except Exception as e:
        print(f"Midtrans error: {e}")
        return None

def check_midtrans_payment_status(order):
    server_key = getattr(settings, 'MIDTRANS_SERVER_KEY', '')
    is_production = getattr(settings, 'MIDTRANS_IS_PRODUCTION', False)
    
    core = midtransclient.CoreApi(
        is_production=is_production,
        server_key=server_key,
        client_key=getattr(settings, 'MIDTRANS_CLIENT_KEY', '')
    )
    
    try:
        response = core.transactions.status(order.order_number)
        return response
    except Exception as e:
        print(f'Midtrans status error: {e}')
        return None

def merge_guest_cart(request, user):
    """
    Memindahkan item dari keranjang session (guest) ke keranjang user yang baru login.
    """
    from orders.models import Cart, CartItem
    session_key = request.session.session_key
    if not session_key:
        return
        
    try:
        guest_cart = Cart.objects.get(session_key=session_key, user=None)
        user_cart, created = Cart.objects.get_or_create(user=user)
        
        # Pindahkan item-item
        for guest_item in guest_cart.items.all():
            user_item, item_created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=guest_item.product,
                size=guest_item.size,
                defaults={'quantity': guest_item.quantity}
            )
            if not item_created:
                # Tambahkan quantity tapi jangan sampai melebihi stok
                new_qty = user_item.quantity + guest_item.quantity
                if new_qty > guest_item.size.stock:
                    new_qty = guest_item.size.stock
                user_item.quantity = new_qty
                user_item.save()
            
            guest_item.delete()
            
        guest_cart.delete()
    except Cart.DoesNotExist:
        pass

