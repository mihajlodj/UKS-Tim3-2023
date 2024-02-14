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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_labels(request):
    labels = Label.objects.all()
    serialized_labels = serialize_labels(labels)
    return Response(serialized_labels, status=status.HTTP_200_OK)


def serialize_labels(labels):
    result = []
    for label in labels:
        result.append(serialize_label(label))
    return result


def serialize_label(label):
    return {
        'id': label.id,
        'name': label.name,
        'description': label.description
    }
