from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string
import threading

from main.models import RegistrationCandidate

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
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])

        registration_candidate = RegistrationCandidate.objects.create(
            user=user,
            code=''.join(random.choice(string.digits) for _ in range(6))
        )
        registration_candidate.save()
        thr = threading.Thread(target=send_email, args=([registration_candidate]), kwargs={})
        thr.start()
        return user


def send_email(registration_candidate):
    subject = 'Confirm your registration to Github Clone'
    html_message = render_to_string('verification_code_email.html', {'code': registration_candidate.code, 'name': registration_candidate.user.first_name})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [registration_candidate.user.email,]
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
