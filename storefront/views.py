from django.shortcuts import render
from products.models import Banner, Product, Category, Brand

def home_view(request):
    banners = Banner.objects.filter(is_active=True).order_by('order', '-id')
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.all().order_by('order')

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, "storefront/home.html", context)

def catalog_view(request):
    query = request.GET.get('q', '')
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort', '-created_at')

    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(name__icontains=query)
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if category_id:
        products = products.filter(category_id=category_id)
        
    if sort in ['-created_at', 'price', '-price']:
        products = products.order_by(sort)

    brands = Brand.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'current_sort': sort,
    }

    if request.headers.get('HX-Request'):
        return render(request, "storefront/partials/product_grid.html", context)
        
    return render(request, "storefront/katalog.html", context)

def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug, is_active=True)
    related_products = Product.objects.filter(brand=product.brand, is_active=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, "storefront/detail.html", context)
