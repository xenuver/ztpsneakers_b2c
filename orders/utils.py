import requests
from django.conf import settings
import midtransclient

def get_rajaongkir_provinces():
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', '')
    url = "https://api.rajaongkir.com/starter/province"
    headers = {"key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('rajaongkir', {}).get('results', [])
    except Exception as e:
        print(f"RajaOngkir error: {e}")
    return []

def get_rajaongkir_cities(province_id):
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', '')
    url = f"https://api.rajaongkir.com/starter/city?province={province_id}"
    headers = {"key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('rajaongkir', {}).get('results', [])
    except Exception as e:
        print(f"RajaOngkir error: {e}")
    return []

def calculate_shipping_cost(origin_city, destination_city, weight, courier):
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', '')
    url = "https://api.rajaongkir.com/starter/cost"
    headers = {"key": api_key, "content-type": "application/x-www-form-urlencoded"}
    payload = f"origin={origin_city}&destination={destination_city}&weight={weight}&courier={courier}"
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('rajaongkir', {}).get('results', [])
    except Exception as e:
        print(f"RajaOngkir error: {e}")
    return []

def generate_midtrans_snap_token(order):
    server_key = getattr(settings, 'MIDTRANS_SERVER_KEY', '')
    client_key = getattr(settings, 'MIDTRANS_CLIENT_KEY', '')
    is_production = False # sandbox
    
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
