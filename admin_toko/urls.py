from django.urls import path
from . import views

app_name = 'admin_toko'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.products_view, name='products'),
    path('products/<int:product_id>/toggle/', views.product_toggle_view, name='product_toggle'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:order_id>/update/', views.order_update_status, name='order_update'),
    path('warranty/', views.warranty_view, name='warranty'),
    path('warranty/<int:claim_id>/update/', views.warranty_update_status, name='warranty_update'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('reviews/<int:review_id>/toggle/', views.review_toggle_view, name='review_toggle'),
    path('customers/', views.customers_view, name='customers'),
]
