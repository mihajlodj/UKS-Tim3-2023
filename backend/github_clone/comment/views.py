from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from main.models import Comment, Issue, Milestone, PullRequest, WorksOn, Role

from comment.serializers import CommentSerializer

from main import permissions

class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_comments_for_type(request, owner_username, repository_name, type_for, type_id):
    is_valid_type_for = valid_type_for(type_for)
    if not is_valid_type_for:
        raise Http404()
    if not type_id.isdigit():
        raise Http404()
    object_exists = check_if_type_id_object_exists(type_id, type_for)
    if not object_exists:
        raise Http404()
    repository = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    comments = find_all_comments(repository, type_for, type_id)
    serialized_comments = serialize_comments(comments)
    return Response(serialized_comments, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,])
def delete_comment(request, owner_username, repository_name, comment_id):
    if not comment_id.isdigit():
        raise Http404()
    if not Comment.objects.filter(id=comment_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def serialize_comments(comments):
    result = []
    for comment in comments:
        if comment.parent is not None:
            continue

        serialized_comment = {
            'id': comment.id,
            'content': comment.content,
            'sub_comments': [],
            'time': comment.time,
            'developer_id': comment.caused_by.id
        }

        # Find sub-comments and add them
        sub_comments = find_sub_comments(comment.id)
        serialized_sub_comments = serialize_sub_comments(sub_comments)
        serialized_comment['sub_comments'].extend(serialized_sub_comments)

        if comment.issue is not None:
            serialized_comment['issue_id'] = comment.issue.id
        elif comment.milestone is not None:
            serialized_comment['milestone_id'] = comment.milestone.id
        elif comment.pull_request is not None:
            serialized_comment['pull_request'] = comment.pull_request.id
        result.append(serialized_comment)
    return result


def serialize_sub_comments(sub_comments):
    result = []
    for comment in sub_comments:
        serialized_comment = {
            'id': comment.id,
            'content': comment.content,
            'time': comment.time,
            'developer_id': comment.caused_by.id
        }
        result.append(serialized_comment)
    return result


def find_sub_comments(comment_id):
    sub_comments = Comment.objects.filter(parent_id=comment_id)
    return sub_comments


def valid_type_for(type_for):
    if type_for == "issue":
        return True
    elif type_for == "milestone":
        return True
    elif type_for == "pull_request":
        return True
    return False


def check_if_type_id_object_exists(type_id, type_for):
    if type_for == "issue":
        return check_if_issue_exists(type_id)
    elif type_for == "milestone":
        return check_if_milestone_exists(type_id)
    elif type_for == "pull_request":
        return check_if_pull_request_exists(type_id)


def check_if_issue_exists(type_id):
    if Issue.objects.filter(id=type_id).exists():
        return True
    return False


def check_if_milestone_exists(type_id):
    if Milestone.objects.filter(id=type_id).exists():
        return True
    return False


def check_if_pull_request_exists(type_id):
    if PullRequest.objects.filter(gitea_id=type_id).exists():
        return True
    return False


def find_all_comments(repository, type_for, type_id):
    if type_for == "issue":
        return find_all_comments_from_issue(type_id)
    elif type_for == "milestone":
        return find_all_comments_from_milestone(type_id)
    elif type_for == "pull_request":
        return find_all_comments_from_pull_request(repository, type_id)


def find_all_comments_from_issue(issue_id):
    issue = Issue.objects.get(id=issue_id)
    return Comment.objects.filter(issue=issue)


def find_all_comments_from_milestone(milestone_id):
    milestone = Milestone.objects.get(id=milestone_id)
    return Comment.objects.filter(milestone=milestone)


def find_all_comments_from_pull_request(repository, pull_request_id):
    pull_request = PullRequest.objects.get(project=repository, gitea_id=pull_request_id)
    return Comment.objects.filter(pull_request=pull_request)
