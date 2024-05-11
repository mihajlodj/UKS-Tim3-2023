import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from issue.serializers import IssueSerializer
from main import gitea_service
from main.models import Developer, Project, WorksOn, Branch, Commit, Release, Tag
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
import json

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username1 = 'miki4'
password = 'kikiriki'
repo_name = 'newrepo1'
def_tag_name = 'default_tag_name'

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

    commit = Commit.objects.create(
        hash='234w56r7t8oyf9pjsdolkfansfnaslkndsa',
        author=dev1,
        committer=dev1,
        branch=branch,
        message="commit message"
    )
    commit.save()
    return dev1, repo, commit, branch


@pytest.fixture(autouse=True)
def save_release(create_dev_and_repo):
    dev1, repo, commit, branch = create_dev_and_repo
    release = Release.objects.create(
        title='default release',
        description='desc',
        target=branch,
        pre_release=False,
        draft=False,
        tag=Tag.objects.create(name=def_tag_name, caused_by=dev1, project=repo),
        commit=commit,
        project=repo
    )
    release.save()



@pytest.fixture
def get_token(create_dev_and_repo):
    dev1, repo, commit, branch = create_dev_and_repo
    url = '/auth/login/'
    payload = {
        'username': dev1.user.username,
        'password': password,
    }
    response = client.post(url, payload)
    return response.data['access']


# RELEASE ######

@pytest.fixture(autouse=True)
def disable_gitea_create_release(monkeypatch):
    def mock_gitea_create_release(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'create_new_release', mock_gitea_create_release)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_delete_release(monkeypatch):
    def mock_gitea_delete_release(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'update_release', mock_gitea_delete_release)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_update_release(monkeypatch):
    def mock_gitea_update_release(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'delete_release', mock_gitea_update_release)
    yield

# TAGS ########

@pytest.fixture(autouse=True)
def disable_gitea_create_tag(monkeypatch):
    def mock_gitea_create_tag(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'create_tag', mock_gitea_create_tag)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_delete_tag(monkeypatch):
    def mock_gitea_delete_tag(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'delete_tag', mock_gitea_delete_tag)
    yield


@pytest.mark.django_db
def test_create_release(get_token):
    url = '/release/miki4/newrepo1/create/'
    data = {
        "title": "new-release2",
        "description": "description of the first release",
        "branch_name": "main",
        "pre_release": False,
        "draft": False,
        "tag_name": "new_tag2",
        "caused_by_username": "miki4"
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    assert Release.objects.count() == 1
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_releases(get_token):
    url = f'/release/miki4/newrepo1/releases/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_update_release(get_token):
    url = f'/release/update/miki4/newrepo1/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    body = {
        "release_id": 1,
        "updated_title": "updated-release1",
        "updated_description": "updated description",
        "updated_pre_release": True,
        "updated_draft": False,
        "updated_tag": "edited-tag=edited"
    }
    response = client.patch(url, data=body, headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_release(get_token):
    url = f'/release/delete/miki4/newrepo1/{def_tag_name}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_release_by_tag_name(get_token):
    url = f'/release/get/miki4/newrepo1/{def_tag_name}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_release_by_id(get_token):
    url = f'/release/miki4/newrepo1/{1}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
