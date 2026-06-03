from django.shortcuts import render
from .models import FooterIcon, Notification

def index(request):
    footer_icons = FooterIcon.objects.all()
    context = {"footer_icons": footer_icons}
    return render(request, "core/homepage.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def all_notifications(request):
    """Halaman daftar semua notifikasi."""
    notifications = request.user.notifications.all()[:50]
    # Tandai semua sebagai dibaca
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, "core/notifications.html", {'notifications': notifications})

@login_required
def notification_count(request):
    """HTMX endpoint: kembalikan badge count notif belum dibaca."""
    count = request.user.notifications.filter(is_read=False).count()
    if count > 0:
        html = f'<span class="absolute -top-1 -right-1 flex h-3 w-3"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-red-500 text-[8px] text-white justify-center items-center font-bold">{count}</span></span>'
        return HttpResponse(html)
    return HttpResponse('')