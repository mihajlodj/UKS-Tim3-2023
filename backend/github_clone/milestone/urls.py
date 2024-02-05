from django.urls import path

from milestone.views import *

urlpatterns = [
    path('create/<str:repository_name>/', CreateMilestoneView.as_view(), name='create_mileestone')
]