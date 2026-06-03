from django.contrib import admin
from django.utils.html import format_html
from .models import Banner,FooterIcon,Brand,Product


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)

@admin.register(FooterIcon)
class FooterIconAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # slug otomatis dari name
    
    def brand_logo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;">', obj.image.url)
        return "-"
    brand_logo_preview.short_description = "Logo"
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "price", "total_sold", "is_active", "created_at")
    list_filter = ("brand", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # slug otomatis
    ordering = ("-created_at",)