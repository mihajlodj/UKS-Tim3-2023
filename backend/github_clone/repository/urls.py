from django.urls import path
from repository.views import CreateRepositoryView, ReadRepositoryView, ReadOwnerView

urlpatterns = [
    path('', CreateRepositoryView.as_view(), name='create_repo'),
    path('owner/<str:username>/', ReadOwnerView.as_view(), name='read_owner'),
    path('<str:owner_username>/<str:repository_name>/', ReadRepositoryView.as_view(), name='read_repo'),
]