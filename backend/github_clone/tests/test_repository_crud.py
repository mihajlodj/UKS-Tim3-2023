import pytest
from django.contrib.auth.models import User

from main import gitea_service
from main.models import Developer, Project, WorksOn, Branch
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker

from repository.serializers import RepositorySerializer

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username = 'MyUsername'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
repo_name2 = 'MyNewTestRepo2'

@pytest.fixture
def create_developer():
    user = User.objects.create_user(username=username, password=password)
    dev = Developer.objects.create(user=user)
    return dev

@pytest.fixture
def get_token(create_developer):
    url = '/auth/login/'
    payload = {
        'username': create_developer.user.username,
        'password': password,
    }
    response = client.post(url, payload)
    return response.data['access']

@pytest.fixture(autouse=True)
def save_repository(create_developer):
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')
    branch = Branch.objects.create(name='main', project=repo)
    Branch.objects.create(name='develop', project=repo, parent=branch)
    repo.default_branch = branch
    repo.save()
    WorksOn.objects.create(role='Owner', project=repo, developer=create_developer)

@pytest.mark.django_db
def test_create_public_repo_success(get_token):
    url = '/repository/'
    repo_data = {
        'name': repo_name2,
        'description': fake.text,
        'access_modifier': 'Public',
        'default_branch_name': 'main',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == repo_name2
    assert Project.objects.count() == 2
    assert WorksOn.objects.count() == 2
    assert Branch.objects.count() == 3

    works_on = WorksOn.objects.get(project__name=repo_name2)
    assert works_on.developer.user.username == username
    assert works_on.role == 'Owner'

@pytest.mark.django_db
def test_create_private_repo_success(get_token):
    url = '/repository/'
    repo_data = {
        'name': repo_name2,
        'description': '',
        'access_modifier': 'Private',
        'default_branch_name': '',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == repo_name2
    assert Project.objects.count() == 2
    assert WorksOn.objects.count() == 2
    assert Branch.objects.count() == 3

    works_on = WorksOn.objects.get(project__name=repo_name2)
    assert works_on.developer.user.username == username
    assert works_on.role == 'Owner'

@pytest.mark.django_db
def test_create_repo_invalid_name(get_token):
    url = '/repository/'
    repo_data = {
        'name': 'This is&invalid',
        'description': fake.text,
        'access_modifier': 'Public',
        'default_branch_name': 'main',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['name'][0] == 'Invalid repository name'
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2


@pytest.mark.django_db
def test_create_repo_invalid_branch_name(get_token):
    url = '/repository/'
    repo_data = {
        'name': repo_name,
        'description': 'This is description',
        'access_modifier': 'Public',
        'default_branch_name': 'main@dev',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['default_branch_name'][0] == 'Invalid branch name'
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2


@pytest.mark.django_db
def test_create_repo_duplicate_name(get_token):
    url = '/repository/'
    repo_data = {
        'name': repo_name,
        'description': fake.text,
        'access_modifier': 'Public',
        'default_branch_name': 'main',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['name'][0] == 'This field must be unique.'
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2


@pytest.fixture(autouse=True)
def disable_gitea_delete_repository(monkeypatch):
    def mock_gitea_delete_repository(*args, **kwargs):
        return

    monkeypatch.setattr(gitea_service, 'delete_repository', mock_gitea_delete_repository)
    yield

@pytest.mark.django_db
def test_delete_repo_success(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/repository/delete/{username}/{repo_name}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Project.objects.count() == 0
    assert WorksOn.objects.count() == 0
    assert Branch.objects.count() == 0


@pytest.mark.django_db
def test_delete_repo_does_not_exist(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/repository/delete/{username}/{repo_name2}/'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2


@pytest.fixture(autouse=True)
def disable_gitea_update(monkeypatch):
    def mock_gitea_update(*args, **kwargs):
        return

    monkeypatch.setattr(RepositorySerializer, 'gitea_update', mock_gitea_update)
    yield
@pytest.mark.django_db
def test_update_repo_success(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/repository/update/{repo_name}/'
    repo_data = {
        'name': 'updated-name',
        'description': fake.text,
        'access_modifier': 'Public',
        'default_branch_name': 'develop',
    }
    response = client.patch(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2
    repo = Project.objects.get(name='updated-name')
    assert repo.access_modifier == 'Public'
    assert repo.default_branch.name == 'develop'
    assert not Project.objects.filter(name=repo_name).exists()

@pytest.mark.django_db
def test_update_repo_invalid_name(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/repository/update/{repo_name}/'
    repo_data = {
        'name': 'updated-name bad',
        'description': fake.text,
        'access_modifier': 'Public',
        'default_branch_name': 'develop',
    }
    response = client.patch(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2
    repo = Project.objects.get(name=repo_name)
    assert repo.access_modifier == 'Private'
    assert repo.default_branch.name == 'main'
    assert not Project.objects.filter(name='updated-name bad').exists()


@pytest.mark.django_db
def test_update_repo_branch_does_not_exist(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/repository/update/{repo_name}/'
    repo_data = {
        'name': 'updated-name',
        'description': fake.text,
        'access_modifier': 'Public',
        'default_branch_name': 'master',
    }
    response = client.patch(url, repo_data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Project.objects.count() == 1
    assert WorksOn.objects.count() == 1
    assert Branch.objects.count() == 2
    repo = Project.objects.get(name=repo_name)
    assert repo.access_modifier == 'Private'
    assert repo.default_branch.name == 'main'
    assert not Project.objects.filter(name='updated-name').exists()