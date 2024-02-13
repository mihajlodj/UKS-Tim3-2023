import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from main.models import Developer, Project, WorksOn, Branch, Issue
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker

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
        manager=dev1,
        created=timezone.now()
    )
    issue.save()

@pytest.mark.django_db
def test_create_issue(get_token):
    # dev2 = create_developers
    # repo = create_repository
    url = '/issue/create/'
    issue_data = {
        'created': timezone.now(),
        'title': 'issue2',
        'description': 'description2',
        'manager': username1,
        'project': repo_name,
        'milestone': '',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, issue_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['project'] == repo_name
    assert response.data['manager'] == username1


@pytest.mark.django_db
def test_get_issues(get_token):
    # dev2 = create_developers
    # repo = create_repository
    url = '/issue/issues/MyNewTestRepo'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.content) == 186
    assert len(response.json()) == 1
    assert response.json()[0]['project'] == repo_name
    assert response.json()[0]['manager'] == username1
    assert response.json()[0]['title'] == 'issue1'
    assert response.json()[0]['description'] == 'description1'
    assert response.json()[0]['id'] == 1
