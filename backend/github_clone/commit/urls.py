from django.urls import path
from commit.views import *

urlpatterns = [
    path('diff/<str:owner_username>/<str:repository_name>/<str:sha>/', get_diff, name='get_diff'),
    path('info/<str:owner_username>/<str:repository_name>/<str:sha>/', get, name='get'),
]