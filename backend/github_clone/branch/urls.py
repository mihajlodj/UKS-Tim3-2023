from django.urls import path
from branch.views import *

urlpatterns = [
    path('all/<str:owner_username>/<str:repository_name>/', get_all_branches, name='get_all_branches'),
]