from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path("entry/", views.entry_view, name="entry"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
]