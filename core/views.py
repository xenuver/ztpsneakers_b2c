from django.shortcuts import render
from .models import FooterIcon

def index(request):
    footer_icons = FooterIcon.objects.all()
    context = {"footer_icons": footer_icons}
    return render(request, "core/homepage.html", context)