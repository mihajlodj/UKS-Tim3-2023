import pytest
from django.contrib.auth.models import User
from requests import Response
from main.models import Developer, Project, WorksOn, Branch, Commit, PullRequest, PullRequestStatus, Milestone
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from main import gitea_service
import json
from django.utils import timezone

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username1 = 'MyUsername'
username2 = 'MyUsername2'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
repo_name2 = 'MyNewTestRepo2'
pull_title = 'Title'


@pytest.fixture
def create_developers():
    user1 = User.objects.create_user(username=username1, password=password)
    dev1 = Developer.objects.create(user=user1)
    user2 = User.objects.create_user(username=username2, password=password)
    dev2 = Developer.objects.create(user=user2)
    return dev1, dev2

@pytest.fixture
def get_token(create_developers):
    url = '/auth/login/'
    payload = {
        'username': create_developers[0].user.username,
        'password': password,
    }
    response = client.post(url, payload)
    return response.data['access']

@pytest.fixture(autouse=True)
def save_repository(create_developers):
    dev1, dev2 = create_developers
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')
    main = Branch.objects.create(name='main', project=repo, created_by=dev1)
    develop = Branch.objects.create(name='develop', project=repo, parent=main, created_by=dev2)
    branch1 = Branch.objects.create(name='branch1', project=repo, parent=develop, created_by=dev2)
    branch2 = Branch.objects.create(name='branch2', project=repo, parent=branch1, created_by=dev1)
    branch3 = Branch.objects.create(name='branch3', project=repo, parent=branch1, created_by=dev1)
    repo.default_branch = main
    repo.save()
    WorksOn.objects.create(role='Owner', project=repo, developer=dev1)
    WorksOn.objects.create(role='Maintainer', project=repo, developer=dev2)
    return repo, main, develop, branch1, branch2, branch3

@pytest.fixture(autouse=True)
def save_pull_requests(create_developers, save_repository):
    dev1, dev2 = create_developers
    repo, main, develop, branch1, branch2, branch3 = save_repository
    milestone = Milestone.objects.create(title='Milestone', deadline=timezone.localtime(timezone.now()), project=Project.objects.get(name=repo_name))
    PullRequest.objects.create(title=pull_title, source=branch3, target=develop, project=repo, author=dev1, status=PullRequestStatus.OPEN, mergeable=True, gitea_id=10)
    PullRequest.objects.create(source=branch1, target=develop, project=repo, author=dev2, status=PullRequestStatus.CLOSED, gitea_id=11)
    PullRequest.objects.create(source=branch2, target=branch1, project=repo, author=dev1, status=PullRequestStatus.MERGED, gitea_id=12)
    PullRequest.objects.create(source=branch3, target=branch1, project=repo, author=dev1, status=PullRequestStatus.OPEN, mergeable=False, gitea_id=13, milestone=milestone)


@pytest.fixture(autouse=True)
def disable_gitea_merge_pull_request(monkeypatch):
    def mock_merge_pull_request(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'merge_pull_request', mock_merge_pull_request)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_create_pull_request(monkeypatch):
    def mock_create_pull_request(*args, **kwargs):
        response = Response()
        content = {'id': 1, 'mergeable': True}
        response.json = lambda: content
        response.status_code = 201
        return response
    monkeypatch.setattr(gitea_service, 'create_pull_request', mock_create_pull_request)
    yield


@pytest.mark.django_db
def test_create_pull_success(get_token):
    url = f'/pr/create/{username1}/{repo_name}/'
    data = {
        'base': 'main',
        'compare': 'develop',
        'title': 'Title',
        'description': 'Description',
        'assignee': username2
    }
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.post(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert PullRequest.objects.count() == 5
    assert PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).status == PullRequestStatus.OPEN

@pytest.mark.django_db
def test_create_pull_bad_assignee_success(get_token):
    url = f'/pr/create/{username1}/{repo_name}/'
    data = {
        'base': 'main',
        'compare': 'develop',
        'title': 'Title',
        'description': 'Description',
        'assignee': 'non-existing'
    }
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.post(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert PullRequest.objects.count() == 5
    assert PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).status == PullRequestStatus.OPEN
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).assignee is None

@pytest.mark.django_db
def test_create_pull_duplicate(get_token):
    url = f'/pr/create/{username1}/{repo_name}/'
    data = {
        'base': 'develop',
        'compare': 'branch3',
        'title': 'Title',
        'description': 'Description',
        'assignee': username2
    }
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.post(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "Pull request already exists"
    assert PullRequest.objects.count() == 4
    assert not PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()

@pytest.mark.django_db
def test_merge_pull_success(get_token):
    url = f'/pr/merge/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).status == PullRequestStatus.MERGED

@pytest.mark.django_db
def test_merge_pull_not_mergeable(get_token):
    url = f'/pr/merge/{repo_name}/13/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=13, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=13, project__name=repo_name).status == PullRequestStatus.OPEN

@pytest.mark.django_db
def test_close_pull_success(get_token):
    url = f'/pr/close/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).status == PullRequestStatus.CLOSED

@pytest.mark.django_db
def test_try_close_merged_pull(get_token):
    url = f'/pr/close/{repo_name}/12/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=12, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=12, project__name=repo_name).status == PullRequestStatus.MERGED

@pytest.mark.django_db
def test_reopen_pull_success(get_token):
    url = f'/pr/reopen/{repo_name}/11/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=11, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=11, project__name=repo_name).status == PullRequestStatus.OPEN

@pytest.mark.django_db
def test_try_open_merged_pull(get_token):
    url = f'/pr/reopen/{repo_name}/12/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=12, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=12, project__name=repo_name).status == PullRequestStatus.MERGED

@pytest.mark.django_db
def test_try_merge_closed_pull(get_token):
    url = f'/pr/merge/{repo_name}/11/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    response = client.put(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=11, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=11, project__name=repo_name).status == PullRequestStatus.CLOSED

@pytest.mark.django_db
def test_assign_milestone_success(get_token):
    milestone = Milestone.objects.create(title='Milestone', deadline=timezone.localtime(timezone.now()), project=Project.objects.get(name=repo_name))
    url = f'/pr/update/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = { 'milestone_id': milestone.id }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).milestone.id == milestone.id

@pytest.mark.django_db
def test_remove_milestone_success(get_token):
    url = f'/pr/update/{repo_name}/13/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = {}
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=13, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=13, project__name=repo_name).milestone is None

@pytest.mark.django_db
def test_assign_milestone_does_not_exist(get_token):
    url = f'/pr/update/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = { 'milestone_id': 1500 }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).milestone is None

@pytest.mark.django_db
def test_assign_developer_success(get_token):
    url = f'/pr/update/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = { 'assignee_username': username1 }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).assignee.user.username == username1

@pytest.mark.django_db
def test_remove_developer_success(get_token):
    url = f'/pr/update/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = {}
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).assignee is None

@pytest.mark.django_db
def test_assign_developer_does_not_exist(get_token):
    url = f'/pr/update/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = { 'assignee_username': 'non-existing' }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).assignee is None

@pytest.mark.django_db
def test_update_title_success(get_token):
    new_title = 'This is the new title'
    url = f'/pr/title/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = { 'title': new_title }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).title == new_title

@pytest.mark.django_db
def test_update_title_empty(get_token):
    new_title = '  '
    url = f'/pr/title/{repo_name}/10/'
    headers = { 'Authorization': f'Bearer {get_token}' }
    data = { 'title': new_title }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullRequest.objects.count() == 4
    assert PullRequest.objects.filter(gitea_id=10, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=10, project__name=repo_name).title == pull_title