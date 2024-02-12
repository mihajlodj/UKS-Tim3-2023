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
username2 = 'MyUsername2'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
repo_name2 = 'MyNewTestRepo2'


@pytest.fixture
def create_developers():
    user1 = User.objects.create_user(username=username1, password=password)
    dev1 = Developer.objects.create(user=user1)
    user2 = User.objects.create_user(username=username2, password=password)
    dev2 = Developer.objects.create(user=user2)
    return dev1, dev2

@pytest.fixture(autouse=True)
def save_repository(create_developer):
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')
    branch = Branch.objects.create(name='main', project=repo)
    Branch.objects.create(name='develop', project=repo, parent=branch)
    repo.default_branch = branch
    repo.save()
    WorksOn.objects.create(role='Owner', project=repo, developer=create_developer)

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
def save_issue(create_developers):
    dev2 = create_developers
    issue = Issue.objects.create(
        created=timezone.now(),
        title='issue1',
        description='description1',
        manager=dev2,
        milestone=None,
        open=True)
