from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('', views.main, name='main-main'),
    path('webhook/', webhooks.webhook, name='webhook'),
]
