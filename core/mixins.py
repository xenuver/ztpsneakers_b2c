from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class AdminTokoRequiredMixin(LoginRequiredMixin):
    """Verify that the current user has the AdminToko role."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin_toko' and request.user.role != 'owner' and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class OwnerRequiredMixin(LoginRequiredMixin):
    """Verify that the current user has the Owner role."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'owner' and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
