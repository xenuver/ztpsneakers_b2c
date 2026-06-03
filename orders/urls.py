from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('cart/', views.cart_view, name='cart_page'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/drawer/', views.cart_drawer, name='cart_drawer'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('api/provinces/', views.get_provinces_options, name='get_provinces_options'),
    path('api/cities/', views.get_cities, name='get_cities'),
    path('api/shipping-cost/', views.get_shipping_cost, name='get_shipping_cost'),
    path('api/update-total/', views.update_total, name='update_total'),
    path('checkout/success/<str:order_number>/', views.checkout_success, name='checkout_success'),
    path('midtrans/webhook/', views.midtrans_webhook, name='midtrans_webhook'),
    path('history/', views.order_history_view, name='history'),
    path('history/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('history/<str:order_number>/invoice/', views.print_invoice, name='print_invoice'),
    path('history/<str:order_number>/complete/', views.complete_order, name='complete_order'),
    path('item/<int:item_id>/review/', views.create_review, name='create_review'),
    path('item/<int:item_id>/warranty/', views.create_warranty_claim, name='create_warranty_claim'),
    path('garansi/<int:claim_id>/', views.warranty_tracking, name='warranty_tracking'),
]
