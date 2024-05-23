from django.urls import path

from milestone.views import *

urlpatterns = [
    path('create/<str:owner_username>/<str:repository_name>/', CreateMilestoneView.as_view(), name='create_mileestone'),
    path('update/<str:owner_username>/<str:title>/', UpdateMilestoneView.as_view(), name='update_milestone'),
    path('delete/<str:owner_username>/<str:repository_name>/<str:title>/', delete_milestone, name='delete_milestone'),
    path('all/<str:owner_username>/<str:repository_name>/', get_milestones_for_repo, name='get_all_milestones'),
    path('one/<str:owner_username>/<str:repository_name>/<str:milestone_id>/', get_milestone, name='get_milestone'),
]