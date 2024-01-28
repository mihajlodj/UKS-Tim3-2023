from django.urls import path
from repository.views import *

urlpatterns = [
    path('', CreateRepositoryView.as_view(), name='create_repo'),
    path('owner/<str:username>/', ReadOwnerView.as_view(), name='read_owner'),
    path('<str:owner_username>/<str:repository_name>/', get_repo_data_for_display, name='read_repo'),
    path('content/<str:owner_username>/<str:repository_name>/<str:ref>/', get_root_files, name='get_root_files'),
]