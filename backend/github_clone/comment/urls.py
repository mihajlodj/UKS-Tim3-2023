from django.urls import path

from comment.views import *

urlpatterns = [
    path('create/', CreateCommentView.as_view(), name='create_comment')
]
