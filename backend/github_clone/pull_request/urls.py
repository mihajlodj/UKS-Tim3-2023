from django.urls import path
from pull_request.views import *

urlpatterns = [
    path('create/<str:owner_username>/<str:repository_name>/', create, name='create'),
    path('get_all/<str:repository_name>/', get_all, name='get_all'),
]