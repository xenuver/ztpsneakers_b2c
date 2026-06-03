from django.contrib import admin
from .models import FooterIcon

@admin.register(FooterIcon)
class FooterIconAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)