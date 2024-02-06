import pytest
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch, Commit
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
def disable_gitea_create_file(monkeypatch):
    def mock_create_file(*args, **kwargs):
        return commit_hash
    monkeypatch.setattr(gitea_service, 'create_file', mock_create_file)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_upload_files(monkeypatch):
    def mock_upload_files(*args, **kwargs):
        return commit_hash
    monkeypatch.setattr(gitea_service, 'upload_files', mock_upload_files)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_delete_file(monkeypatch):
    def mock_delete_file(*args, **kwargs):
        return commit_hash
    monkeypatch.setattr(gitea_service, 'delete_file', mock_delete_file)
    yield

@pytest.fixture(autouse=True)
def disable_gitea_get_file(monkeypatch):
    def mock_get_file(*args, **kwargs):
        return {
            'sha': '1234'
        }
    monkeypatch.setattr(gitea_service, 'get_file', mock_get_file)
    yield


@pytest.mark.django_db
def test_create_file_success(get_token):
    url = f'/repository/create_file/{username1}/{repo_name}/file.txt/'
    data = {
        'content': 'This is some content',
        'branch': 'main',
        'message': 'this is a commit message',
        'additional_text': 'some description',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Commit.objects.count() == 1
    assert Commit.objects.get(hash=commit_hash).message == 'this is a commit message'


@pytest.mark.django_db
def test_upload_files_success(get_token):
    url = f'/repository/upload/{username2}/{repo_name}/'
    data = {
        'branch': 'main',
        'message': 'this is a commit message',
        'additional_text': 'some description',
        'files': [
            {
                'name': 'file1.txt',
                'content': 'U29tZSBtb3JlIGNvbnRlbnQ='
            },
            {
                'name': 'file2.txt',
                'content': 'U29tZSBtb3JlIGNvbnRlbnQxMjM0NQ=='
            }
        ]
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Commit.objects.count() == 1
    assert Commit.objects.get(hash=commit_hash).message == 'this is a commit message'


@pytest.mark.django_db
def test_delete_file_success(get_token):
    url = f'/repository/delete_file/{username1}/{repo_name}/file.txt/'
    data = {
        'branch': 'main',
        'message': 'this is a commit message',
        'additional_text': 'some description',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.put(url, content_type='application/json', data=json.dumps(data), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Commit.objects.count() == 1
    assert Commit.objects.get(hash=commit_hash).message == 'this is a commit message'
