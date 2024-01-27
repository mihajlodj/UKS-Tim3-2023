from django.urls import path
from repository.views import CreateRepositoryView, ReadRepositoryView

urlpatterns = [
    path('', CreateRepositoryView.as_view(), name='create_repo'),
    path('read/', ReadRepositoryView.as_view(), name='read_repo'),
]