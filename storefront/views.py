from django.shortcuts import render
from products.models import Banner, Product, Category, Brand

from django.db.models import Sum
from django.db.models.functions import Coalesce

def home_view(request):
    banners = Banner.objects.filter(is_active=True).order_by('order', '-id')
    
    from django.db.models import Case, When, Value, IntegerField, OuterRef, Subquery
    from products.models import ProductSize

    stock_subquery = ProductSize.objects.filter(product=OuterRef('pk')).values('product').annotate(
        total=Sum('stock')
    ).values('total')
    
    bestseller_products = Product.objects.filter(is_active=True).annotate(
        total_sold=Coalesce(Sum('orderitem__quantity'), 0),
        annotated_stock=Coalesce(Subquery(stock_subquery, output_field=IntegerField()), 0)
    ).annotate(
        is_sold_out=Case(When(annotated_stock__gt=0, then=Value(0)), default=Value(1), output_field=IntegerField())
    ).order_by('is_sold_out', '-total_sold')[:10]
    
    new_products = Product.objects.filter(is_active=True).annotate(
        annotated_stock=Coalesce(Subquery(stock_subquery, output_field=IntegerField()), 0)
    ).annotate(
        is_sold_out=Case(When(annotated_stock__gt=0, then=Value(0)), default=Value(1), output_field=IntegerField())
    ).order_by('is_sold_out', '-created_at')[:10]
    categories = Category.objects.all().order_by('order')

    wishlist_product_ids = []
    if request.user.is_authenticated:
        from orders.models import Wishlist
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    from django.db.models import Avg
    
    # Hot items (rating >= 4.5)
    hot_items = Product.objects.filter(is_active=True).annotate(
        annotated_stock=Coalesce(Subquery(stock_subquery, output_field=IntegerField()), 0)
    ).annotate(
        is_sold_out=Case(When(annotated_stock__gt=0, then=Value(0)), default=Value(1), output_field=IntegerField())
    ).annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__gte=4.5).order_by('is_sold_out', '-avg_rating')[:8]
    
    # Brands for strip
    brands = Brand.objects.all().order_by('name')
    
    registration_voucher = None
    if request.user.is_authenticated:
        from orders.models import Voucher
        registration_voucher = Voucher.objects.filter(
            user=request.user, 
            is_active=True, 
            is_used=False,
            code__startswith='WELCOME-'
        ).first()

    context = {
        'banners': banners,
        'registration_voucher': registration_voucher,
        'bestseller_products': bestseller_products,
        'new_products': new_products,
        'hot_items': hot_items,
        'brands': brands,
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
    
    selected_colors = request.GET.getlist('color')
    if len(selected_colors) == 1 and ',' in selected_colors[0]:
        selected_colors = [c for c in selected_colors[0].split(',') if c]
    else:
        selected_colors = [c for c in selected_colors if c]
        
    selected_sizes = request.GET.getlist('size')
    if len(selected_sizes) == 1 and ',' in selected_sizes[0]:
        selected_sizes = [s for s in selected_sizes[0].split(',') if s]
    else:
        selected_sizes = [s for s in selected_sizes if s]
    
    condition = request.GET.get('condition', '')

    from django.db.models import Case, When, Value, IntegerField, OuterRef, Subquery
    from products.models import ProductSize
    
    stock_subquery = ProductSize.objects.filter(product=OuterRef('pk')).values('product').annotate(
        total=Sum('stock')
    ).values('total')

    products = Product.objects.filter(is_active=True).annotate(
        annotated_stock=Coalesce(Subquery(stock_subquery, output_field=IntegerField()), 0)
    ).annotate(
        is_sold_out=Case(
            When(annotated_stock__gt=0, then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    )
    
    if query:
        products = products.filter(name__icontains=query)
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if category_id:
        # Support both numeric ID and category name/slug
        if str(category_id).isdigit():
            products = products.filter(category_id=category_id)
        else:
            products = products.filter(category__name__iexact=category_id)
    if selected_colors:
        products = products.filter(color__in=selected_colors)
    if selected_sizes:
        products = products.filter(sizes__size__in=selected_sizes).distinct()
    if condition in ['new', 'second']:
        products = products.filter(condition=condition)
        
    if sort == 'featured':
        products = products.filter(is_featured=True).order_by('is_sold_out', '-created_at')
    elif sort == 'newest':
        products = products.order_by('is_sold_out', '-created_at')
    elif sort == 'hot':
        from django.db.models import Avg
        products = products.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=4.0).order_by('is_sold_out', '-avg_rating')
    elif sort == 'bestseller':
        from orders.models import OrderItem
        sold_subquery = OrderItem.objects.filter(product=OuterRef('pk')).values('product').annotate(
            total=Sum('quantity')
        ).values('total')
        products = products.annotate(
            total_sold=Coalesce(Subquery(sold_subquery, output_field=IntegerField()), 0)
        ).order_by('is_sold_out', '-total_sold')
    elif sort in ['-created_at', 'price', '-price']:
        products = products.order_by('is_sold_out', sort)
    else:
        products = products.order_by('is_sold_out', '-created_at')

    paginator = Paginator(products, 12) # 12 items per page
    page_obj = paginator.get_page(page_number)

    brands = Brand.objects.all()
    categories = Category.objects.all()
    all_colors = Product.COLOR_CHOICES
    
    from products.models import ProductSize
    all_sizes = ProductSize.objects.values_list('size', flat=True).distinct().order_by('size')
    
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
        'sizes': all_sizes,
        'selected_sizes': selected_sizes,
        'condition': condition,
        'current_sort': sort,
        'query': query,
        'brand_id': brand_id,
        'category_id': category_id,
        'wishlist_product_ids': wishlist_product_ids,
    }

    if request.headers.get('HX-Request'):
        return render(request, "storefront/partials/product_grid.html", context)
        
    return render(request, "storefront/katalog.html", context)

from django.shortcuts import get_object_or_404
def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(brand=product.brand, is_active=True).exclude(id=product.id)[:4]
    
    wishlist_product_ids = []
    if request.user.is_authenticated:
        from orders.models import Wishlist
        wishlist_product_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    reviews = product.reviews.filter(is_visible=True)
    total_reviews = reviews.count()
    
    rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    if total_reviews > 0:
        for r in reviews:
            if r.rating in rating_distribution:
                rating_distribution[r.rating] += 1
        
        # Calculate percentages
        for k in rating_distribution:
            rating_distribution[k] = int((rating_distribution[k] / total_reviews) * 100)

    context = {
        'product': product,
        'related_products': related_products,
        'wishlist_product_ids': wishlist_product_ids,
        'rating_distribution': rating_distribution,
    }
    return render(request, "storefront/detail.html", context)

def live_search_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, "storefront/partials/search_results.html", {'products': []})
        
    products = Product.objects.filter(is_active=True, name__icontains=query).order_by('-created_at')[:5]
    return render(request, "storefront/partials/search_results.html", {'products': products})
