import pytest
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch, Fork
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from main import gitea_service
import json

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username1 = 'MyUsername'
username2 = 'MyUsername2'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
repo_name2 = 'MyNewTestRepo2'
commit_hash = '12345'

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

@pytest.fixture
def get_token2(create_developers):
    url = '/auth/login/'
    payload = {
        'username': create_developers[1].user.username,
        'password': password,
    }
    response = client.post(url, payload)
    return response.data['access']

@pytest.fixture
def get_token_not_collaborator():
    user = User.objects.create_user(username='not_collab', password=password)
    Developer.objects.create(user=user)

    url = '/auth/login/'
    payload = {
        'username': 'not_collab',
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
    Branch.objects.create(name='branch2', project=repo, parent=branch1, created_by=dev1)
    repo.default_branch = main
    repo.save()
    WorksOn.objects.create(role='Owner', project=repo, developer=dev1)
    WorksOn.objects.create(role='Maintainer', project=repo, developer=dev2)

@pytest.fixture(autouse=True)
def disable_gitea_fork(monkeypatch):
    def mock_fork(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'fork', mock_fork)
    yield


@pytest.mark.django_db
def test_fork_success(get_token2):
    headers = {
        'Authorization': f'Bearer {get_token2}'
    }
    url = f'/repository/fork/{username1}/{repo_name}/'
    payload = {'name': repo_name, 'description': ''}
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Fork.objects.filter().count() == 1
    assert Project.objects.filter().count() == 2


@pytest.mark.django_db
def test_fork_own_repository(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/repository/fork/{username1}/{repo_name}/'
    payload = {'name': repo_name, 'description': ''}
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Fork.objects.filter().count() == 0
    assert Project.objects.filter().count() == 1


@pytest.mark.django_db
def test_fork_private_repository_not_collaborator(get_token_not_collaborator):
    headers = {
        'Authorization': f'Bearer {get_token_not_collaborator}'
    }
    url = f'/repository/fork/{username1}/{repo_name}/'
    payload = {'name': repo_name, 'description': ''}
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Fork.objects.filter().count() == 0
    assert Project.objects.filter().count() == 1


# try change visibility of private forked repository