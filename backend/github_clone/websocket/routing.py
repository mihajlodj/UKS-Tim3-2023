from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/notify/<str:username>/', consumers.NotificationConsumer.as_asgi()),
]