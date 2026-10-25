from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    t_filter = request.GET.get('type')
    if t_filter:
        notifications = notifications.filter(notification_type=t_filter)

    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'current_filter': t_filter
    })


@login_required
def mark_as_read(request, notification_id):
    notif = get_object_or_404(Notification, id=notification_id, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link_url:
        return redirect(notif.link_url)
    return redirect('notification_list')


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('notification_list')
