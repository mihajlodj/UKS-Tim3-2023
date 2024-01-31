from django.urls import path
from branch.views import *

urlpatterns = [
    path('all/<str:owner_username>/<str:repository_name>/', get_all_branches, name='get_all_branches'),
    path('create/<str:created_by>/<str:repository_name>/', CreateBranchView.as_view(), name='create_branch'),
]