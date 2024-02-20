from django.urls import path
from pull_request.views import *

urlpatterns = [
    path('create/<str:owner_username>/<str:repository_name>/', create, name='create'),
    path('get_all/<str:repository_name>/', get_all, name='get_all'),
    path('get/<str:repository_name>/<int:pull_id>/', get_one, name='get_one'),
    path('assignees/<str:repository_name>/', get_possible_assignees, name='get_possible_assignees'),
    path('update/<str:repository_name>/<int:pull_id>/', update, name='update'),
    path('title/<str:repository_name>/<int:pull_id>/', update_title, name='update_title'),
    path('close/<str:repository_name>/<int:pull_id>/', close, name='close'),
    path('reopen/<str:repository_name>/<int:pull_id>/', reopen, name='reopen'),
]