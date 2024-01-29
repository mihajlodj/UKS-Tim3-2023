from django.urls import path
from repository.views import *

urlpatterns = [
    path('', CreateRepositoryView.as_view(), name='create_repo'),
    path('owner/<str:username>/', ReadOwnerView.as_view(), name='read_owner'),
    path('update/<str:name>/', UpdateRepositoryView.as_view(), name='update_repository'),
    path('delete/<str:owner_username>/<str:repository_name>/', delete_repo, name='read_repo'),
    path('<str:owner_username>/<str:repository_name>/', get_repo_data_for_display, name='read_repo'),
    path('content/<str:owner_username>/<str:repository_name>/<str:ref>/', get_root_files, name='get_root_files'),
    path('folder/<str:owner_username>/<str:repository_name>/<str:branch>/<path:path>/', get_folder_files, name='get_root_files'),
]