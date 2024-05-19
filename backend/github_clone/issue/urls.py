from django.urls import path
from issue.views import *

urlpatterns = [
    path('create/', IssueView.as_view(), name='create_issue'),
    path('query_issues/<str:query>/', get_all_issues, name='get_all_issues'),
    path('<int:pk>/', get_issue, name='get_issue'),
    path('<str:repo_name>/<int:pk>/', delete_issue, name='delete_issue'),
    path('close/<str:repo_name>/<int:pk>/', close_issue, name='delete_issue'),
    path('reopen/<str:repo_name>/<int:pk>/', reopen_issue, name='reopen_issue'),
    path('update/', update_issue, name='update_issue'),
    path('issues/<str:owner_username>/<str:repo_name>/', get_issues, name='get_dev_issues'),
    path('<str:owner_username>/<str:repo_name>/managers/assign/', assign_manager, name='assign_manager'),
    path('<str:owner_username>/<str:repo_name>/managers/un_assign/', unassign_manager, name='un_assign_manager'),
    path('<str:owner_username>/<str:repo_name>/managers/<int:issue_id>/', get_possible_assignees, name='get_possible_assignees'),
]
