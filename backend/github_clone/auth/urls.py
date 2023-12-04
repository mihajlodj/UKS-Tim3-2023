from django.urls import path
from auth.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
]
