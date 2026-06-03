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

def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        # TODO: return message or redirect
        return HttpResponse("""<script>window.location.href='/';</script>""")
        
    from .utils import get_rajaongkir_provinces
    provinces = get_rajaongkir_provinces()
    
    context = {
        'cart': cart,
        'provinces': provinces,
    }
    return render(request, "orders/checkout.html", context)
