from django.urls import path
from issue.views import *

urlpatterns = [
    path('create/', IssueView.as_view(), name='create_issue'),
    path('<int:pk>/', get_issue, name='get_issue'),
    path('<str:repo_name>/<int:pk>/', delete_issue, name='delete_issue'),
    path('close/<str:repo_name>/<int:pk>/', close_issue, name='delete_issue'),
    path('update/', update_issue, name='update_issue'),
    path('issues/<str:repo_name>/', get_issues, name='get_dev_issues')
]
