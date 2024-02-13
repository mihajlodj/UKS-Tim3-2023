from django.urls import path

from comment.views import *

urlpatterns = [
    path('create/', CreateCommentView.as_view(), name='create_comment'),
    path('all/<str:type_for>/<str:type_id>', get_comments_for_type, name='get_comments_for_type')
]
