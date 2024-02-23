import requests
from django.conf import settings
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from datetime import datetime

from issue.serializers import IssueSerializer
from main.models import Developer, Issue

gitea_base_url = settings.GITEA_BASE_URL
access_token = settings.GITEA_ACCESS_TOKEN

