from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('django-main/', views.main, name='main-main'),
    path('django-main/webhook/', webhooks.webhook, name='webhook'),
]
