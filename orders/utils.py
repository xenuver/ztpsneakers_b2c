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
        
    # Fallback dummy shipping cost for Komerce structure
    dummy_costs = {
        'jne': [{'code': 'jne', 'service': 'REG', 'cost': 15000, 'etd': '2-3'}, {'code': 'jne', 'service': 'YES', 'cost': 25000, 'etd': '1'}],
        'pos': [{'code': 'pos', 'service': 'Kilat Khusus', 'cost': 14000, 'etd': '2-4'}],
        'tiki': [{'code': 'tiki', 'service': 'ECO', 'cost': 12000, 'etd': '3-5'}, {'code': 'tiki', 'service': 'ONS', 'cost': 22000, 'etd': '1'}]
    }
    return dummy_costs.get(courier, [])

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
