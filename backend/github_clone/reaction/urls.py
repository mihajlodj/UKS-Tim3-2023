from django.urls import path

from reaction.views import *

urlpatterns = [
    path('create/<str:owner_username>/<str:repository_name>/', CreateReactionView.as_view(), name='create_reaction'),
]
