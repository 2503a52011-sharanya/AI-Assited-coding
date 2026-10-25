from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        unread_qs = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'unread_notifications_count': unread_qs.count(),
            'recent_notifications': unread_qs[:5]
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }
