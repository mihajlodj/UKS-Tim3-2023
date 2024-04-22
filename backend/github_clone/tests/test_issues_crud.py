import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from issue.serializers import IssueSerializer
from main import gitea_service
from main.models import Developer, Project, WorksOn, Branch, Issue
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
import json

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username1 = 'MyUsername'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'


@pytest.fixture
def create_dev_and_repo():
    user1 = User.objects.create_user(username=username1, password=password)
    dev1 = Developer.objects.create(user=user1)
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')
    branch = Branch.objects.create(name='main', project=repo)
    Branch.objects.create(name='develop', project=repo, parent=branch)
    repo.default_branch = branch
    repo.save()
    WorksOn.objects.create(role='Owner', project=repo, developer=dev1)
    return dev1, repo

@pytest.fixture
def get_token(create_dev_and_repo):
    dev1, repo = create_dev_and_repo
    url = '/auth/login/'
    payload = {
        'username': dev1.user.username,
        'password': password,
    }
    response = client.post(url, payload)
    return response.data['access']

@pytest.fixture(autouse=True)
def save_issue(create_dev_and_repo):
    dev1, repo = create_dev_and_repo
    issue = Issue.objects.create(
        title='issue1',
        description='description1',
        open=True,
        milestone=None,
        project=repo,
        creator=dev1,
        created=timezone.now()
    )
    issue.save()

@pytest.fixture(autouse=True)
def disable_gitea_create_issue(monkeypatch):
    def mock_gitea_create_issue(*args, **kwargs):
        return

    monkeypatch.setattr(IssueSerializer, 'create_issue_in_gitea', mock_gitea_create_issue)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_close_issue(monkeypatch):
    def mock_gitea_close_issue(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'close_issue', mock_gitea_close_issue)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_delete_issue(monkeypatch):
    def mock_gitea_delete_issue(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'delete_issue', mock_gitea_delete_issue)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_update_issue(monkeypatch):
    def mock_gitea_update_issue(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'update_issue', mock_gitea_update_issue)
    yield

@pytest.mark.django_db
def test_create_issue(get_token):

    url = '/issue/create/'
    issue_data = {
        'created': timezone.now(),
        'title': 'issue2',
        'description': 'description2',
        'creator': username1,
        # 'manager': None,
        'project': repo_name,
        'milestone': '',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    assert Issue.objects.count() == 1
    response = client.post(url, issue_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['project'] == repo_name
    assert response.data['creator'] == username1


@pytest.mark.django_db
def test_get_issues(get_token):
    url = f'/issue/issues/{username1}/MyNewTestRepo/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.content) == 186
    assert len(response.json()) == 1
    assert response.json()[0]['project'] == repo_name
    assert response.json()[0]['creator'] == username1
    assert response.json()[0]['title'] == 'issue1'
    assert response.json()[0]['description'] == 'description1'
    assert response.json()[0]['id'] == 1

@pytest.mark.django_db
def test_get_issues(get_token):
    url = f'/issue/issues/{username1}/MyNewTestRepo/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.content) == 186
    assert len(response.json()) == 1
    assert response.json()[0]['project'] == repo_name
    assert response.json()[0]['creator'] == username1
    assert response.json()[0]['title'] == 'issue1'
    assert response.json()[0]['description'] == 'description1'
    assert response.json()[0]['id'] == 1

@pytest.mark.django_db
def test_close_issue(get_token):
    url = '/issue/close/MyNewTestRepo/1/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.patch(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f'/issue/issues/{username1}/MyNewTestRepo/', headers=headers)
    assert response.json()[0]['open'] is False

@pytest.mark.django_db
def test_delete_issues(get_token):

    url = '/issue/MyNewTestRepo/1/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f'/issue/issues/{username1}/MyNewTestRepo/', headers=headers)
    assert len(response.json()) == 0

@pytest.mark.django_db
def test_update_issue(get_token):
    # dev1, repo = create_dev_and_repo
    url = '/issue/update/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    body = {
        'id': 1,
        'title': 'new_issue_title',
        'description': 'new_description',
        'milestone': '',
        'repoName': repo_name
    }
    response_get_old = client.get(f'/issue/issues/{username1}/MyNewTestRepo/', headers=headers)
    assert response_get_old.status_code == status.HTTP_200_OK
    assert response_get_old.json()[0]['title'] == 'issue1'
    assert response_get_old.json()[0]['description'] == 'description1'
    response_post = client.patch(url, content_type='application/json', data=json.dumps(body), headers=headers)
    assert response_post.status_code == status.HTTP_200_OK

    response_get_new = client.get(f'/issue/issues/{username1}/MyNewTestRepo/', headers=headers)
    assert response_get_new.status_code == status.HTTP_200_OK
    assert response_get_new.json()[0]['title'] == 'new_issue_title'
    assert response_get_new.json()[0]['description'] == 'new_description'

@pytest.mark.django_db
def test_delete_issues_2(get_token):

    url = '/issue/MyNewTestRepo/3/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_get_issues_2(get_token):
    url = f'/issue/issues/{username1}/MyNewTestRepo2/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.content) == 2
    assert len(response.json()) == 0
