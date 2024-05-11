from django.urls import path
from release.views import *

urlpatterns = [
    path('<str:owner_username>/<str:project_name>/create/', create_new_release, name='create_new_release'),
    path('<str:owner_username>/<str:project_name>/releases/', get_releases, name='get_releases'),
    path('delete/<str:owner_username>/<str:project_name>/<str:tag_name>/', delete_release, name='delete_releases'),
    path('get/<str:owner_username>/<str:project_name>/<str:tag_name>/', get_release_by_tag_name, name='get_release_by_tag_name'),
    path('<str:owner_username>/<str:project_name>/<int:release_id>/', get_release_by_id, name='get_release_by_id'),
    path('update/<str:owner_username>/<str:project_name>/', update_release, name='get_release_by_id'),
]
