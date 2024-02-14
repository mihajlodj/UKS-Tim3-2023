from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Label

from label.serializers import LabelSerializer

class CreateLabelView(generics.CreateAPIView):
    queryset = Label.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LabelSerializer
