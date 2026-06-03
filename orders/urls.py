from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/drawer/', views.cart_drawer, name='cart_drawer'),
    path('checkout/', views.checkout_view, name='checkout'),
]
