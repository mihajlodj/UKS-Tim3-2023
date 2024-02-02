from django.urls import path
from developer.views import *

urlpatterns = [
    path('update/<str:username>/', UpdateUserView.as_view(), name='update_developer_username'),
]