from django.shortcuts import render
from products.models import Banner, Product, Category, Brand

def home_view(request):
    banners = Banner.objects.filter(is_active=True).order_by('order', '-id')
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.all().order_by('order')

    wishlist_product_ids = []
    if request.user.is_authenticated:
        from orders.models import Wishlist
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'categories': categories,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, "storefront/home.html", context)

from django.core.paginator import Paginator

def catalog_view(request):
    query = request.GET.get('q', '')
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort', '-created_at')
    page_number = request.GET.get('page', 1)
    color_param = request.GET.get('color', '')
    selected_colors = [c for c in color_param.split(',') if c]

    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(name__icontains=query)
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if category_id:
        products = products.filter(category_id=category_id)
    if selected_colors:
        products = products.filter(color__in=selected_colors)
        
    if sort in ['-created_at', 'price', '-price']:
        products = products.order_by(sort)

    paginator = Paginator(products, 12) # 12 items per page
    page_obj = paginator.get_page(page_number)

    brands = Brand.objects.all()
    categories = Category.objects.all()
    all_colors = Product.COLOR_CHOICES
    
    wishlist_product_ids = []
    if request.user.is_authenticated:
        from orders.models import Wishlist
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'products': page_obj,
        'brands': brands,
        'categories': categories,
        'colors': all_colors,
        'selected_colors': selected_colors,
        'current_sort': sort,
        'query': query,
        'brand_id': brand_id,
        'category_id': category_id,
        'wishlist_product_ids': wishlist_product_ids,
    }

    if request.headers.get('HX-Request'):
        return render(request, "storefront/partials/product_grid.html", context)
        
    return render(request, "storefront/katalog.html", context)

def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug, is_active=True)
    related_products = Product.objects.filter(brand=product.brand, is_active=True).exclude(id=product.id)[:4]
    
    wishlist_product_ids = []
    if request.user.is_authenticated:
        from orders.models import Wishlist
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    context = {
        'product': product,
        'related_products': related_products,
        'wishlist_product_ids': wishlist_product_ids,
    }
    return render(request, "storefront/detail.html", context)

def live_search_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, "storefront/partials/search_results.html", {'products': []})
        
    products = Product.objects.filter(is_active=True, name__icontains=query).order_by('-created_at')[:5]
    return render(request, "storefront/partials/search_results.html", {'products': products})
