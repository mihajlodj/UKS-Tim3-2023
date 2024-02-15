from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string
import threading
from main.models import RegistrationCandidate
from main.gitea_service import save_user
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token
    

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        registration_candidate = RegistrationCandidate.objects.create(
            user=user,
            code=''.join(random.choice(string.digits) for _ in range(6)),
            created_at=timezone.now()
        )
        registration_candidate.save()
        threading.Thread(target=self.send_email, args=([registration_candidate]), kwargs={}).start()
        self.save_gitea_user(user, validated_data['password'])
        return user

    def send_email(self, registration_candidate):
        subject = 'Confirm your registration to Github Clone'
        html_message = render_to_string('verification_code_email.html', {'code': registration_candidate.code, 'name': registration_candidate.user.first_name})
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [registration_candidate.user.email,]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)

    def save_gitea_user(self, user, password):
        save_user({
            'username': user.username,
            'password': password,
            'email': user.email,
            'full_name': user.get_full_name(),
            'must_change_password': False
        })

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad token')
