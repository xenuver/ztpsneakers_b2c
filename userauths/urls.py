from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('auth/login-tab/', views.login_tab, name='login_tab'),
    path('auth/register-tab/', views.register_tab, name='register_tab'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]