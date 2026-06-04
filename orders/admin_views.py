from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count

@staff_member_required
def dashboard_analytics_api(request):
    """API for Jazzmin dashboard (Owner)"""
    today = timezone.now().date()
    
    # 1. KPI Cards
    # Total Revenue This Month
    current_month_orders = Order.objects.filter(
        created_at__year=today.year, 
        created_at__month=today.month,
        status__in=['paid', 'processing', 'shipped', 'completed']
    )
    total_revenue_month = current_month_orders.aggregate(Sum('total'))['total__sum'] or 0
    
    # Total Order (All time)
    total_orders = Order.objects.count()
    
    # New Customers This Month
    from userauths.models import User
    new_customers = User.objects.filter(
        date_joined__year=today.year,
        date_joined__month=today.month,
        is_staff=False,
        is_superuser=False
    ).count()
    
    # Top Products (All time)
    from products.models import Product
    from orders.models import OrderItem
    top_products = OrderItem.objects.filter(
        order__status__in=['paid', 'processing', 'shipped', 'completed']
    ).values('product_name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:5]
    
    top_products_list = [{'name': p['product_name'], 'sold': p['total_sold']} for p in top_products]

    # 2. Sales Chart (Last 4 weeks)
    chart_labels = []
    chart_data = []
    
    for i in range(3, -1, -1):
        start_date = today - timedelta(days=(i*7)+6)
        end_date = today - timedelta(days=i*7)
        
        week_orders = Order.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            status__in=['paid', 'processing', 'shipped', 'completed']
        )
        week_revenue = week_orders.aggregate(Sum('total'))['total__sum'] or 0
        
        # Convert to Millions for the chart if it's large, or just keep raw
        week_revenue_million = float(week_revenue) / 1000000.0
        
        label = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}"
        chart_labels.append(label)
        chart_data.append(round(week_revenue_million, 2))

    # 3. Heatmap Data (Orders count by day and hour)
    from django.db.models.functions import ExtractWeekDay, ExtractHour
    heatmap_qs = Order.objects.filter(
        status__in=['paid', 'processing', 'shipped', 'completed']
    ).annotate(
        weekday=ExtractWeekDay('created_at'),
        hour=ExtractHour('created_at')
    ).values('weekday', 'hour').annotate(count=Count('id'))

    # Weekday mapping in Django (1=Sunday, 2=Monday, ..., 7=Saturday)
    days_map = {2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat', 1: 'Sun'}
    heatmap_data = []
    
    for item in heatmap_qs:
        day_str = days_map.get(item['weekday'], 'Mon')
        hour_str = f"{item['hour']:02d}:00"
        heatmap_data.append({
            'x': day_str,
            'y': hour_str,
            'v': item['count']
        })

    # 4. Recent Sales (Laporan Penjualan Terakhir)
    recent_orders_qs = Order.objects.filter(
        status__in=['paid', 'processing', 'shipped', 'completed']
    ).order_by('-created_at')[:10]
    
    recent_orders = []
    for o in recent_orders_qs:
        recent_orders.append({
            'order_number': o.order_number,
            'user': o.user.email if o.user else 'Guest',
            'date': o.created_at.strftime('%d %b %Y %H:%M'),
            'total': float(o.total),
            'status': o.get_status_display()
        })

    data = {
        'kpis': {
            'total_revenue_month': total_revenue_month,
            'total_orders': total_orders,
            'new_customers': new_customers,
            'top_products': top_products_list
        },
        'chart': {
            'labels': chart_labels,
            'data': chart_data
        },
        'heatmap': heatmap_data,
        'recent_orders': recent_orders
    }
    
    return JsonResponse(data)
