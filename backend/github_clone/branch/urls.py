from django.urls import path
from branch.views import *

urlpatterns = [
    path('all/<str:owner_username>/<str:repository_name>/', get_all_branches, name='get_all_branches'),
    path('create/<str:owner_username>/<str:created_by>/<str:repository_name>/', CreateBranchView.as_view(), name='create_branch'),
    path('delete/<str:owner_username>/<str:repository_name>/<str:branch_name>/', delete_branch, name='get_all_branches'),
    path('commits/<str:owner_username>/<str:repository_name>/<str:branch_name>/', get_commits, name='get_commits'),
    path('committers/<str:owner_username>/<str:repository_name>/<str:branch_name>/', get_committers, name='get_committers'),
]