from main.models import RegistrationCandidate, Developer
from .serializers import RegistrationSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from main.gitea_service import save_user

gitea_base_url = 'http://localhost:3000'
access_token = '9bd445fd68c2a34b4f7348e3578956ad49216b83'

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def confirm_registration(request):
    username = request.data.get('username')
    code = request.data.get('code').strip()
    try:
        registration_candidate = RegistrationCandidate.objects.get(user__username=username)
        if registration_candidate.code == code:
            registration_candidate.user.is_active = True
            registration_candidate.user.save()
            dev = Developer.objects.create(user=registration_candidate.user)
            dev.save()
            registration_candidate.delete()
            save_user({
                'username': dev.user.username,
                'password': dev.user.password,
                'email': dev.user.email,
                'full_name': dev.user.get_full_name()
            })
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect registration code.'}, status=status.HTTP_404_NOT_FOUND)
    except RegistrationCandidate.DoesNotExist:
        return Response({'error': 'Registration candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
    