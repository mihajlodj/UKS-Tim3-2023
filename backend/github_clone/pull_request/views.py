from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from main import gitea_service, permissions
import json
from main.models import PullRequest, Branch, Developer, WorksOn, Role, PullRequestStatus, PullRequestReviewStatus, \
    PullRequestReview, EventHistory
from pull_request import diff_parser, service
from developer import service as developer_service
from repository.serializers import RepositorySerializer, DeveloperSerializer
from django.core.cache import cache
from datetime import datetime
from websocket import notification_service
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import threading


@api_view(['POST'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def create(request, owner_username, repository_name):
    json_data = json.loads(request.body.decode('utf-8'))
    project = WorksOn.objects.get(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).project
    if PullRequest.objects.filter(project=project, source__name=json_data['compare'], target__name=json_data['base']):
        return Response("Pull request already exists", status=status.HTTP_400_BAD_REQUEST)
    if not Branch.objects.filter(name=json_data['base'], project=project).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not Branch.objects.filter(name=json_data['compare'], project=project).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    title = service.get_pull_title(json_data)
    response = gitea_service.create_pull_request(owner_username, repository_name,
                                                 {'base': json_data['base'], 'head': json_data['compare'],
                                                  'title': title})
    print(response.status_code)
    if response.status_code == 201:
        id = service.save_pull_request(owner_username, request.user.username, repository_name, json_data, response)
        pr_info = {
            'initiated_by': request.user.username,
            'src': json_data['compare'],
            'dest': json_data['base'],
            'assignee': '',
            'reviewers': [],
            'id': id,
            'title': title,
            'author': request.user.username
        }
        threading.Thread(target=notification_service.send_notification_pull_request_created, args=([owner_username, project, pr_info]), kwargs={}).start()
        return Response({'id': id}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, owner_username, repository_name, pull_id):
    try:
        created_by_username = request.auth.get('username', None)
        works_on = WorksOn.objects.filter(role='Owner', project__name=repository_name, developer__user__username=owner_username)
        project = works_on.first().project

        if not works_on.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        json_data = json.loads(request.body.decode('utf-8'))
        reviewer_username = json_data['reviewer']
        review_comment = json_data['comment']

        review_status = json_data['status']
        # Validate the status
        if review_status not in PullRequestReviewStatus.values:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        pull_request = PullRequest.objects.get(project=project, gitea_id=pull_id)
        reviewer = Developer.objects.get(user__username=reviewer_username)

        # Validate logged in user is reviewer
        print(created_by_username)
        print(reviewer.user.username)
        if created_by_username != reviewer.user.username:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Validate that author of PR is not reviewer
        if reviewer.user.username == pull_request.author.user.username:         # if author of pull request is reviewer return 403 Forbiden, cause author of PR can't create review
            return Response(status=status.HTTP_403_FORBIDDEN)

        pull_request_review = PullRequestReview.objects.create(pull_request=pull_request, reviewer=reviewer, comment=review_comment, status=review_status)
        pull_request_review.save()
        serialized_review = serialize_pull_request_review(pull_request_review)

        assignee = ''
        if pull_request.assignee is not None:
            assignee = pull_request.assignee.user.username
        review_info = {
            'creator': reviewer.user.username,
            'pr_title': pull_request.title,
            'pr_id': pull_request.gitea_id,
            'pr_author': pull_request.author.user.username,
            'pr_assignee': assignee,
            'pr_reviewers': [obj['username'] for obj in service.get_reviwers(pull_request)]
        }
        threading.Thread(target=notification_service.send_notification_review_for_pr_added,
                         args=([owner_username, project, review_info]), kwargs={}).start()

        EventHistory.objects.create(project=project,related_id=pull_request.gitea_id,text=f"Review {reviewer.user.username} added a review {review_status}")
        return Response(serialized_review, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist:
        raise Http404()
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviews_for_pr(request, owner_username, repository_name, pull_id):
    try:
        created_by_username = request.auth.get('username', None)
        works_on = WorksOn.objects.get(role='Owner', project__name=repository_name, developer__user__username=owner_username)

        pull_request = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)

        pull_request_reviews = PullRequestReview.objects.filter(pull_request=pull_request)
        serialized_reviews = serialize_pull_request_reviews(pull_request_reviews)
        return Response(serialized_reviews, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise Http404()
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


def serialize_pull_request_reviews(pull_request_reviews):
    result = []
    for review in pull_request_reviews:
        result.append(serialize_pull_request_review(review))
    return result


def serialize_pull_request_review(pull_request_review):
    return {
        'id': pull_request_review.id,
        'pull_request_id': pull_request_review.pull_request.gitea_id,
        'reviewer_id' : pull_request_review.reviewer.id,
        'comment': pull_request_review.comment,
        'status': pull_request_review.status,
        'timestamp': pull_request_review.timestamp,
    }



@api_view(['GET'])
def get_all_pull_reqs(request, query):
    creator = ''
    is_open = None
    created_date = None
    assignee = ''

    parts = query.split('&')
    for part in parts:
        if 'owner:' in part:
            creator = part.split('owner:', 1)[1].strip()
        elif 'is:' in part:
            is_open = True if part.split('is:', 1)[1].strip() == 'open' else False
        elif 'assignee:' in part:
            assignee = part.split('assignee:', 1)[1].strip()
        elif 'created:' in part:
            created_date = datetime.strptime(part.split('created:', 1)[1].strip(), '%d-%m-%Y').date()
        else:
            query = part.strip()

    print(creator, "->creator", is_open, "->is_open", assignee, "->assignee", created_date, "->created_date", query,
          "->query")

    cache_key = f"pull_request_query:{query}:{creator}:{is_open}:{assignee}:{created_date}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data, status=status.HTTP_200_OK)

    results = PullRequest.objects.all()

    if query:
        results = results.filter(title__contains=query)
    if creator:
        results = results.filter(author__user__username__contains=creator)
    if assignee:
        results = results.filter(assignee__user__username__contains=assignee)
    if is_open is not None:
        if is_open:
            results = results.filter(status__contains="open")
        if not is_open:
            results = results.filter(status__contains="closed")
    if created_date:
        results = results.filter(timestamp__gt=created_date)

    if results.exists():
        serialized_data = []
        for result in results:
            developer_serializer = DeveloperSerializer(result.author)
            author = developer_serializer.data

            project_serializer = RepositorySerializer(result.project)
            project = project_serializer.data

            worksOn = WorksOn.objects.get(project__name=project['name'], role__exact="Owner")

            serialized_data.append(
                {'title': result.title, 'timestamp': result.timestamp, 'project': project, 'author': author,
                 'Status': result.status, 'developer': worksOn.developer.user.username, 'pr_id':result.gitea_id})

        cache.set(cache_key, serialized_data, timeout=30)

        return Response(serialized_data, status=status.HTTP_200_OK)
    else:
        return Response([], status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_all(request, owner_username, repository_name):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    requests = PullRequest.objects.filter(project=works_on.project)
    result = []
    for req in requests:
        obj = {
            'title': req.title, 'status': req.status, 'timestamp': req.timestamp, 'author': {'username': req.author.user.username, 'avatar': developer_service.get_dev_avatar(req.author.user.username)},
            'id': req.gitea_id,
            'labels': [], 'reviews': []
        }
        if req.milestone is not None:
            obj['milestone'] = req.milestone.title
        if req.assignee is not None:
            obj['assignee'] = { 'username': req.assignee.user.username, 'avatar': developer_service.get_dev_avatar(req.assignee.user.username) }
        result.append(obj)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users_prs(request):

    requests = PullRequest.objects.filter(author__user__username=request.user.username)
    result = []
    for req in requests:
        project = req.project
        owner = WorksOn.objects.get(project=project,role=Role.OWNER).developer
        obj = {
            'title': req.title, 'status': req.status, 'timestamp': req.timestamp, 'author': req.author.user.username,
            'id': req.gitea_id,
            'labels': [], 'reviews': [], 'repo_name' :project.name, 'owner_username':owner.user.username
        }
        if req.milestone is not None:
            obj['milestone'] = req.milestone.title
        if req.assignee is not None:
            obj['assignee'] = { 'username': req.assignee.user.username, 'avatar': developer_service.get_dev_avatar(req.assignee.user.username) }
        result.append(obj)
    return Response(result, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_one(request, owner_username, repository_name, pull_id):
    # Basic data
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    if not PullRequest.objects.filter(project=works_on.project, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)
    result = {
        'title': req.title, 'status': req.status, 'timestamp': req.timestamp,
        'author': {'username': req.author.user.username}, 'id': pull_id,
        'labels': [], 'reviews': [], 'reviewers': [], 'mergeable': req.mergeable, 'base': req.target.name,
        'compare': req.source.name,
        'commits': [], 'conflicting_files': [], 'description': req.description
    }
    if req.milestone is not None:
        result['milestone'] = {'id': req.milestone.id, 'title': req.milestone.title}
    if req.assignee is not None:
        result['assignee'] = {'username': req.assignee.user.username, 'avatar': developer_service.get_dev_avatar(req.assignee.user.username)}
    result['reviewers'] = service.get_reviwers(req)

    # Commits data
    response = gitea_service.get_pull_request_commits(owner_username, repository_name, pull_id)
    commits_list_json = response.json()
    for commit_data in commits_list_json:
        result['commits'].append({
            'hash': commit_data['sha'],
            'message': commit_data['commit']['message'],
            'timestamp': commit_data['created'],
            'author': service.get_commit_author(commit_data['author']['login'], commit_data['commit']['message'],
                                                repository_name),
            'files': commit_data['files'],
            'stats': commit_data['stats']
        })

    # Labels data
    from_req_labels = req.labels.all()
    for label in from_req_labels:
        result['labels'].append({
            'id': label.id,
            'name': label.name,
            'description': label.description
        })

    # Diff
    response = gitea_service.get_pull_request_diff(owner_username, repository_name, pull_id)
    diff, overall_additions, overall_deletions = diff_parser.parse_diff(response.text)
    result['diff'] = diff
    result['overall_additions'] = overall_additions
    result['overall_deletions'] = overall_deletions
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, permissions.CanViewRepository])
def get_possible_assignees(request, owner_username, repository_name):
    result = []
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    works_on_list = WorksOn.objects.filter(project=works_on.project)
    for obj in works_on_list:
        if obj.role != Role.IS_BANNED:
            result.append({'username': obj.developer.user.username, 'avatar': developer_service.get_dev_avatar(obj.developer.user.username)})
    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def update(request, owner_username, repository_name, pull_id):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    if not PullRequest.objects.filter(project=works_on.project, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)
    old_assignee = req.assignee
    json_data = json.loads(request.body.decode('utf-8'))
    service.update_milestone(json_data, req)
    req = service.update_assignee(json_data, req, owner_username, repository_name)
    new_assignee = req.assignee
    if (old_assignee is None and new_assignee is not None) or (old_assignee is not None and new_assignee is not None and \
        old_assignee.user.username != new_assignee.user.username):
        pr_info = get_pr_info(req, request)
        threading.Thread(target=notification_service.send_notification_pull_request_changed_assignee, args=([owner_username, works_on.project, pr_info]), kwargs={}).start()
        
    service.update_reviewers(json_data, req, owner_username, repository_name, request)
    EventHistory.objects.create(project=works_on.project, related_id=req.gitea_id,
                                text=f"User {request.user.username} updated pull request")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def update_title(request, owner_username, repository_name, pull_id):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    if not PullRequest.objects.filter(project=works_on.project, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)
    title = json.loads(request.body.decode('utf-8'))['title']
    if title.strip() != '':
        req.title = title
        req.save()
        EventHistory.objects.create(project=works_on.project, related_id=req.gitea_id,
                                    text=f"User {request.user.username} updated pull request title")
        return Response(title, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def close(request, owner_username, repository_name, pull_id):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    if not PullRequest.objects.filter(project=works_on.project, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)
    if req.status != PullRequestStatus.OPEN:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    req.status = PullRequestStatus.CLOSED
    req.timestamp = timezone.localtime(timezone.now())
    req.save()
    pr_info = get_pr_info(req, request)
    threading.Thread(target=notification_service.send_notification_pull_request_closed, args=([owner_username, works_on.project, pr_info]), kwargs={}).start()
    EventHistory.objects.create(project=works_on.project, related_id=req.gitea_id,
                                text=f"User {request.user.username} closed pull request")
    return Response(req.status, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def reopen(request, owner_username, repository_name, pull_id):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    if not PullRequest.objects.filter(project=works_on.project, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)
    if req.status != PullRequestStatus.CLOSED:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    req.status = PullRequestStatus.OPEN
    req.timestamp = timezone.localtime(timezone.now())
    req.save()
    pr_info = get_pr_info(req, request)
    threading.Thread(target=notification_service.send_notification_pull_request_reopened, args=([owner_username, works_on.project, pr_info]), kwargs={}).start()
    EventHistory.objects.create(project=works_on.project, related_id=req.gitea_id,
                                text=f"User {request.user.username} reopened pull request")
    return Response(req.status, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def mark_as_open(request, owner_username, repository_name):
    pull_ids = json.loads(request.body.decode('utf-8'))['ids']
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    for id in pull_ids:
        if PullRequest.objects.filter(project=works_on.project, gitea_id=id).exists():
            pull = PullRequest.objects.get(project=works_on.project, gitea_id=id)
            if pull.status == PullRequestStatus.CLOSED:
                pull.status = PullRequestStatus.OPEN
                pull.timestamp = timezone.localtime(timezone.now())
                pull.save()
                pr_info = get_pr_info(pull, request)
                threading.Thread(target=notification_service.send_notification_pull_request_reopened, args=([owner_username, works_on.project, pr_info]), kwargs={}).start()
                EventHistory.objects.create(project=works_on.project, related_id=pull.gitea_id,
                                            text=f"User {request.user.username} reopened pull request")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def mark_as_closed(request, owner_username, repository_name):
    pull_ids = json.loads(request.body.decode('utf-8'))['ids']
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    for id in pull_ids:
        if PullRequest.objects.filter(project=works_on.project, gitea_id=id).exists():
            pull = PullRequest.objects.get(project=works_on.project, gitea_id=id)
            if pull.status == PullRequestStatus.OPEN:
                pull.status = PullRequestStatus.CLOSED
                pull.timestamp = timezone.localtime(timezone.now())
                pr_info = get_pr_info(pull, request)
                threading.Thread(target=notification_service.send_notification_pull_request_closed, args=([owner_username, works_on.project, pr_info]), kwargs={}).start()
                pull.save()
                EventHistory.objects.create(project=works_on.project, related_id=pull.gitea_id,
                                            text=f"User {request.user.username} closed pull request")
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, permissions.CanEditRepositoryContent])
def merge(request, owner_username, repository_name, pull_id):
    works_on = WorksOn.objects.filter(developer__user__username=owner_username, project__name=repository_name, role=Role.OWNER).first()
    if not PullRequest.objects.filter(project=works_on.project, gitea_id=pull_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    req = PullRequest.objects.get(project=works_on.project, gitea_id=pull_id)
    if req.status != PullRequestStatus.OPEN or not req.mergeable:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    req.status = PullRequestStatus.MERGED
    req.timestamp = timezone.localtime(timezone.now())
    merged_by = Developer.objects.get(user__username=request.user.username)
    req.merged_by = merged_by
    req.save()
    gitea_service.merge_pull_request(owner_username, repository_name, pull_id)
    pr_info = get_pr_info(req, request)
    service.update_commits_after_merge(req)
    threading.Thread(target=notification_service.send_notification_pull_request_merged, args=([owner_username, works_on.project, pr_info]), kwargs={}).start()
    EventHistory.objects.create(project=works_on.project, related_id=req.gitea_id,
                                text=f"User {request.user.username} merged pull request")
    return Response(status=status.HTTP_200_OK)


def get_pr_info(pull, request):
    assignee = ''
    if pull.assignee != None:
        assignee = pull.assignee.user.username
    return {
        'initiated_by': request.user.username,
        'src': pull.source.name,
        'dest': pull.target.name,
        'assignee': assignee,
        'reviewers': [obj['username'] for obj in service.get_reviwers(pull)],
        'id': pull.gitea_id,
        'title': pull.title,
        'author': pull.author.user.username
    }
