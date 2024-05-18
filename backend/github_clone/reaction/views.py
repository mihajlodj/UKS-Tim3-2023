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


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def get_reactions(request, owner_username, repository_name, comment_id):
    if not Comment.objects.filter(id=comment_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    reactions = Reaction.objects.filter(comment_id=comment_id)
    serialized_reactions = serialize_reactions(reactions)
    return Response(serialized_reactions, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.CanEditRepository])
def delete_reaction(request, owner_username, repository_name, reaction_id):
    if not reaction_id.isdigit():
        raise Http404()
    if not Reaction.objects.filter(id=reaction_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    reaction = Reaction.objects.get(id=reaction_id)
    reaction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def serialize_reactions(reactions):
    result = []
    for reaction in reactions:
        result.append(serialize_reaction(reaction))
    return result


def serialize_reaction(reaction):
    return {
        'id': reaction.id,
        'code': reaction.code,
        'comment_id': reaction.comment.id,
        'developer_id': reaction.developer.id,
    }
