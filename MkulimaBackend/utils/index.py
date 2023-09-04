# this helper will help to return all notification sent to given user...
from MkulimaBackend.mkulima.models import *
from django.contrib.auth import get_user_model

def notificationsByUser(user_id): 
    user = get_user_model().objects.get(id=user_id)
    notifications = reversed(Notification.objects.filter(receiver = user).filter(isDeleted = False))
    
    return notifications