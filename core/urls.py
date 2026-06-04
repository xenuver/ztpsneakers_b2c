from django.urls import path
from django.views.generic import TemplateView
from core.views import index, mark_notifications_read, all_notifications, notification_count

app_name = "core"

urlpatterns = [
    path("", index, name="home"),
    path("notifications/", all_notifications, name="all_notifications"),
    path("notifications/read/", mark_notifications_read, name="mark_notifications_read"),
    path("notifications/count/", notification_count, name="notification_count"),
    
    # Static pages
    path("faq/", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),
    path("privacy-policy/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
    path("return-policy/", TemplateView.as_view(template_name="pages/return_policy.html"), name="return_policy"),
    path("about-us/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("contact-us/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
]