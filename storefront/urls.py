from django.urls import path
from . import views

app_name = "storefront"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("katalog/", views.catalog_view, name="catalog"),
    path("produk/<slug:slug>/", views.product_detail_view, name="product_detail"),
]
