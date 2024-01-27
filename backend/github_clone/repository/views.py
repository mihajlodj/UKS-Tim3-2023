from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import generics, status
from main.models import Project

from repository.serializers import RepositorySerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_view(request):
    print('Here in test view')
    return Response(status=status.HTTP_200_OK)


class CreateRepositoryView(generics.CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RepositorySerializer
