from .models import AnnouncementReadStatus, Alumni

def unread_announcement_count(request):
    if request.user.is_authenticated:
        alumni = Alumni.objects.filter(user=request.user).first()
        if alumni:
            count = AnnouncementReadStatus.objects.filter(alumni=alumni, read=False).count()
            return {'unread_announcement_count': count}
    return {'unread_announcement_count': 0}
