from django.urls import path
# Trigger reload
from . import views

app_name = "userauths"

urlpatterns = [
    path('auth/', views.auth_main, name='auth_main'),
    path('auth/check/', views.auth_check, name='auth_check'),
    path('auth/login/', views.auth_login, name='auth_login'),
    path('auth/register/', views.auth_register, name='auth_register'),
    path('auth/logout/', views.auth_logout, name='auth_logout'),
    path('profile/', views.auth_profile, name='profile'),
]