"""
URL configuration for ztpsneakers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/export-excel/', include([
        path('', getattr(__import__('orders.admin_export', fromlist=['export_excel_admin_view']), 'export_excel_admin_view'), name='admin_export_excel'),
    ])),
    path('admin/', admin.site.urls),
    path("",include("storefront.urls")),
    path("pesanan/", include("orders.urls")),
    path("user/", include("userauths.urls")),
    path("accounts/", include("allauth.urls")),
    path("core/", include("core.urls")),
    path("admintoko/", include("admintoko.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)