from django.urls import path

from label.views import *

urlpatterns = [
    path('create/<str:repository_name>/', CreateLabelView.as_view(), name='create_label'),
    path('all/<str:repository_name>/', get_labels, name='get_labels'),
    path('delete/<str:label_id>/', delete_label, name='delete_label')
]
