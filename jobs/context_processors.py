from .models import Notification


def notification_count(request):

    if (
        request.user.is_authenticated
        and request.user.user_type == "employer"
    ):

        unread = Notification.objects.filter(
            employer=request.user,
            is_read=False
        ).count()

        return {
            "unread_notifications_count": unread,
            "candidate_unread_notifications_count": 0,
        }

    if request.user.is_authenticated and request.user.user_type == "candidate":
        unread = Notification.objects.filter(candidate=request.user, is_read=False).count()
        return {"candidate_unread_notifications_count": unread, "unread_notifications_count": 0}

    return {"unread_notifications_count": 0, "candidate_unread_notifications_count": 0}
