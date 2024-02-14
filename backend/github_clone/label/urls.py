from django.urls import path

from label.views import *

urlpatterns = [
    path('create/', CreateLabelView.as_view(), name='create_label'),
    path('all/', get_labels, name='get_labels')
]
