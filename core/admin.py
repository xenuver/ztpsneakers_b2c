from django.contrib import admin
from .models import FooterIcon, StoreSetting

@admin.register(FooterIcon)
class FooterIconAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(StoreSetting)
class StoreSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)