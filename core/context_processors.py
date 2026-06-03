from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_notifications = request.user.notifications.filter(is_read=False)
        return {
            'unread_notifications_count': unread_notifications.count(),
            'latest_notifications': request.user.notifications.all()[:5]
        }
    return {
        'unread_notifications_count': 0,
        'latest_notifications': []
    }
