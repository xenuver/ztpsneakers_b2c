from django.shortcuts import render
from .models import FooterIcon

def index(request):
    footer_icons = FooterIcon.objects.all()
    context = {"footer_icons": footer_icons}
    return render(request, "core/homepage.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))