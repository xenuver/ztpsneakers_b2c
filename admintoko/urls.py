from django.urls import path
from . import views

app_name = 'admintoko'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.products_view, name='products'),
    path('products/add/', views.product_create_view, name='product_create'),
    path('products/<int:product_id>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:product_id>/toggle/', views.product_toggle_view, name='product_toggle'),
    path('category/add/', views.category_create_view, name='category_create'),
    path('brand/add/', views.brand_create_view, name='brand_create'),
    path('categories/', views.categories_view, name='categories'),
    path('brands/', views.brands_view, name='brands'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:order_id>/update/', views.order_update_status, name='order_update'),
    path('warranty/', views.warranty_view, name='warranty'),
    path('warranty/<int:claim_id>/update/', views.warranty_update_status, name='warranty_update'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('reviews/<int:review_id>/toggle/', views.review_toggle_view, name='review_toggle'),
    path('customers/', views.customers_view, name='customers'),
]
