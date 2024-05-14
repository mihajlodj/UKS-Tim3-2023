from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Reaction, Comment, Milestone, Issue, PullRequest

from reaction.serializers import ReactionSerializer

from main import permissions

class CreateReactionView(generics.CreateAPIView):
    queryset = Reaction.objects.all()
    permission_classes = (IsAuthenticated, permissions.CanEditRepository)
    serializer_class = ReactionSerializer
