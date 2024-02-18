from django.urls import path

from label.views import *

urlpatterns = [
    path('create/<str:repository_name>/', CreateLabelView.as_view(), name='create_label'),
    path('all/<str:repository_name>/', get_labels, name='get_labels'),
    path('delete/<str:label_id>/', delete_label, name='delete_label'),
    path('update/<str:id>/', UpdateLabelView.as_view(), name='update_label'),
    path('link/milestone/<str:label_id>/<str:milestone_id>/', link_label_to_milestone, name='link_label_to_milestone'),
    path('link/issue/<str:label_id>/<str:issue_id>/', link_label_to_issue, name='link_label_to_issue')
]
