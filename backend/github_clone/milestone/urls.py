from django.urls import path

from milestone.views import *

urlpatterns = [
    path('create/<str:repository_name>/', CreateMilestoneView.as_view(), name='create_mileestone'),
    path('update/<str:title>/', UpdateMilestoneView.as_view(), name='update_milestone'),
    path('delete/<str:owner_username>/<str:repository_name>/<str:title>/', delete_milestone, name='delete_milestone')
]