from django.shortcuts import render
from .models import Banner, FooterIcon, Brand, Product


def index(request):
    banners = Banner.objects.filter(is_active=True)
    footer_icons = FooterIcon.objects.all()
    
    # Recommended For You: produk terlaris
    recommended_products = (
        Product.objects.filter(is_active=True)
        .order_by("-total_sold", "-created_at")[:10]
    )
    
    # Brand Popular: misal ambil 5 brand pertama
    popular_brands = Brand.objects.all()[:5]
    
    
    context = {
        "recommended_products": recommended_products,
        "popular_brands": popular_brands,
        "banners": banners,
        "footer_icons": footer_icons
    }
    
    return render(request, "core/homepage.html", context)