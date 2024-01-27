from django.urls import path
from repository.views import CreateRepositoryView, test_view

urlpatterns = [
    path('test/', test_view, name='repo-test'),
    path('', CreateRepositoryView.as_view(), name='create_repo'),
]