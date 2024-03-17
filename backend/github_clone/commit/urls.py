from django.urls import path
from commit.views import *

urlpatterns = [
    path('diff/<str:repository_name>/<str:sha>/', get_diff, name='get_diff'),
]