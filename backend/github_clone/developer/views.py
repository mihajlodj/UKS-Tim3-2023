from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from developer.serializers import DeveloperSerializer, UserSerializer
from main.models import Developer
from repository.views import check_view_permission


class UpdateDeveloperView(generics.UpdateAPIView):
    queryset = Developer.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DeveloperSerializer
    lookup_field = 'user'


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'username'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_info(request, username):
    user = User.objects.get(username=username)
    serializer_class = UserSerializer(user)
    print(serializer_class.data)
    return Response(serializer_class.data,status=status.HTTP_200_OK)
