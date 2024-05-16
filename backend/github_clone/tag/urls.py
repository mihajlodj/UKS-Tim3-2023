from django.urls import path
from tag.views import *

urlpatterns = [
    path('<str:owner_username>/<str:project_name>/tags/', get_tags, name='get_tags'),
    path('<str:owner_username>/<str:project_name>/tag/<int:tag_id>', delete_tag, name='delete_tag'),
]
