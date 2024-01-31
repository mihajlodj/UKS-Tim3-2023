import pytest
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch
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


@pytest.mark.django_db
def test_get_all_branches(get_token):
    url = f'/branch/all/{repo_name}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4

@pytest.mark.django_db
def test_create_branch_success(get_token):
    url = f'/branch/create/{username1}/{repo_name}/'
    data = {
        'name': 'new-branch',
        'parent': 'main'
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'new-branch'
    assert Branch.objects.count() == 5
    
@pytest.mark.django_db
def test_create_branch_invalid_name(get_token):
    url = f'/branch/create/{username1}/{repo_name}/'
    data = {
        'name': 'new-branch 123%',
        'parent': 'main'
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Branch.objects.count() == 4

@pytest.mark.django_db
def test_create_branch_invalid_parent(get_token):
    url = f'/branch/create/{username1}/{repo_name}/'
    data = {
        'name': 'new-branch',
        'parent': 'main1'
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Branch.objects.count() == 4

@pytest.mark.django_db
def test_delete_branch_success(get_token):
    branch_name = 'branch1'
    url = f'/branch/delete/{repo_name}/{branch_name}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Branch.objects.count() == 3

@pytest.mark.django_db
def test_delete_branch_does_not_exist(get_token):
    branch_name = 'branch123'
    url = f'/branch/delete/{repo_name}/{branch_name}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Branch.objects.count() == 4