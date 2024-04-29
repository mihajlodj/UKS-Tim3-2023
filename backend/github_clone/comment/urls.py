from django.urls import path

from comment.views import *

urlpatterns = [
    path('create/<str:owner_username>/<str:repository_name>/', CreateCommentView.as_view(), name='create_comment'),
    path('all/<str:owner_username>/<str:repository_name>/<str:type_for>/<str:type_id>', get_comments_for_type, name='get_comments_for_type'),
    path('delete/<str:owner_username>/<str:repository_name>/<str:comment_id>/', delete_comment, name='delete_comment')
]
