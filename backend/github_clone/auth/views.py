from django.shortcuts import render

from main.models import RegistrationCandidate, Developer
from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_registration(request):
    username = request.data.get('username')
    code = request.data.get('code').strip()
    try:
        registration_candidate = RegistrationCandidate.objects.get(user__username=username)
        print(registration_candidate.code)
        print(code)
        if registration_candidate.code == code:
            dev = Developer.objects.create(user=registration_candidate.user)
            dev.save()
            registration_candidate.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect registration code.'}, status=status.HTTP_404_NOT_FOUND)
    except RegistrationCandidate.DoesNotExist:
        return Response({'error': 'Registration candidate not found.'}, status=status.HTTP_404_NOT_FOUND)