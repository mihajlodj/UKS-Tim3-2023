from django.urls import path

from label.views import *

urlpatterns = [
    path('create/<str:owner_username>/<str:repository_name>/', CreateLabelView.as_view(), name='create_label'),
    path('all/<str:owner_username>/<str:repository_name>/', get_labels, name='get_labels'),
    path('delete/<str:owner_username>/<str:repository_name>/<str:label_id>/', delete_label, name='delete_label'),
    path('update/<str:owner_username>/<str:repository_name>/<str:id>/', UpdateLabelView.as_view(), name='update_label'),
    path('link/milestone/<str:owner_username>/<str:repository_name>/<str:label_id>/<str:milestone_id>/', link_label_to_milestone, name='link_label_to_milestone'),
    path('link/issue/<str:owner_username>/<str:repository_name>/<str:label_id>/<str:issue_id>/', link_label_to_issue, name='link_label_to_issue'),
    path('link/pull_request/<str:owner_username>/<str:repository_name>/<str:label_id>/<str:pull_request_id>/', link_label_to_pull_request, name='link_label_to_pull_request')
]
