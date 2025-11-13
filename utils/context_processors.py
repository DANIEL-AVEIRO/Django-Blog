from myapp.models import NotificationModel


def noti_count(request):
    notifications = NotificationModel.objects.all()
    return {"notifications": notifications}
