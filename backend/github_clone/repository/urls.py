from django.urls import path
from repository.views import *

urlpatterns = [
    path('', CreateRepositoryView.as_view(), name='create_repo'),
    path('all_repos/<str:owner_username>/',get_all_users_repo , name='get_all_user_repos'),
    path('owner/<str:username>/', ReadOwnerView.as_view(), name='read_owner'),
    path('update/<str:name>/', UpdateRepositoryView.as_view(), name='update_repository'),
    path('delete/<str:owner_username>/<str:repository_name>/', delete_repo, name='read_repo'),
    path('<str:owner_username>/<str:repository_name>/', get_repo_data_for_display, name='read_repo'),
    path('content/<str:owner_username>/<str:repository_name>/<str:ref>/', get_root_files, name='get_root_files'),
    path('folder/<str:owner_username>/<str:repository_name>/<str:branch>/<path:path>/', get_folder_files, name='get_root_files'),
    path('file/<str:owner_username>/<str:repository_name>/<str:branch>/<path:path>/', get_file, name='get_files'),
    path('edit_file/<str:owner_username>/<str:repository_name>/<path:path>/', edit_file, name='edit_file'),
    path('delete_file/<str:owner_username>/<str:repository_name>/<path:path>/', delete_file, name='delete_file'),
    path('create_file/<str:owner_username>/<str:repository_name>/<path:path>/', create_file, name='create_file'),
    path('upload/<str:owner_username>/<str:repository_name>/', upload_files, name='upload_files'),
]