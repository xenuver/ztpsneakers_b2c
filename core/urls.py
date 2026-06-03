from django.urls import path
from core.views import index, mark_notifications_read, all_notifications, notification_count

app_name = "core"

urlpatterns = [
    path("", index, name="home"),
    path("notifications/", all_notifications, name="all_notifications"),
    path("notifications/read/", mark_notifications_read, name="mark_notifications_read"),
    path("notifications/count/", notification_count, name="notification_count"),
]