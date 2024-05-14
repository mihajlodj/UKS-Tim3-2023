from django.urls import path
from websocket.views import *

urlpatterns = [
    path('', get_notifications, name='get_notifications'),
    path('mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
]