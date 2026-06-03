from django.urls import path
from core.views import index, mark_notifications_read

app_name = "core"

urlpatterns = [
    path("", index, name="home"),
    path("notifications/read/", mark_notifications_read, name="mark_notifications_read"),
]