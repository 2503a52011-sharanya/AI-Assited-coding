from django.db import models
from apps.accounts.models import User

class Notification(models.Model):
    TYPE_CHOICES = (
        ('booking', 'Booking Update'),
        ('weather', 'Weather Advisory / Itinerary Change'),
        ('payment', 'Payment Notification'),
        ('system', 'System Alert'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    link_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.user.username}"

def send_notification(user, title, message, notification_type='system', link_url=''):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link_url=link_url
    )
