import pytest
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch, Milestone
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from main import gitea_service
from milestone.serializers import MilestoneSerializer
from websocket import notification_service

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


@pytest.fixture(autouse=True)
def disable_gitea_create_milestone(monkeypatch):
    def mock_create_milestone(*args, **kwargs):
        return 2
    monkeypatch.setattr(gitea_service, 'create_milestone', mock_create_milestone)
    yield

@pytest.fixture(autouse=True)
def disable_save_gitea_user(monkeypatch):
    def mock_gitea_create_milestone(*args, **kwargs):
        return 2
    monkeypatch.setattr(MilestoneSerializer, 'gitea_create_milestone', mock_gitea_create_milestone)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_update_milestone(monkeypatch):
    def mock_update_milestone(*args, **kwargs):
        return
    monkeypatch.setattr(MilestoneSerializer, 'gitea_update_milestone', mock_update_milestone)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_delete_milestone_from_gitea(monkeypatch):
    def mock_delete_milestone_from_gitea(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'delete_milestone_from_gitea', mock_delete_milestone_from_gitea)
    yield

@pytest.fixture(autouse=True)
def disable_save_gitea_user(monkeypatch):
    def mock_gitea_create_milestone(*args, **kwargs):
        return 2
    monkeypatch.setattr(MilestoneSerializer, 'gitea_create_milestone', mock_gitea_create_milestone)
    yield


@pytest.fixture(autouse=True)
def disable_send_notification(monkeypatch):
    def mock_send_notification(*args, **kwargs):
        return
    monkeypatch.setattr(notification_service, 'send_notification_milestone_created', mock_send_notification)
    monkeypatch.setattr(notification_service, 'send_notification_milestone_edited', mock_send_notification)
    monkeypatch.setattr(notification_service, 'send_notification_milestone_deleted', mock_send_notification)
    monkeypatch.setattr(notification_service, 'send_notification_milestone_closed', mock_send_notification)
    monkeypatch.setattr(notification_service, 'send_notification_milestone_reopened', mock_send_notification)
    yield

# CREATE

@pytest.mark.django_db
def test_create_milestone_success(get_token):
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': 'Milestone40',
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Milestone40'
    assert Milestone.objects.count() == 1


@pytest.mark.django_db
def test_create_milestone_missing_title(get_token):
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Milestone.objects.count() == 0


@pytest.mark.django_db
def test_create_milestone_blank_title(get_token):
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': '',
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Milestone.objects.count() == 0


@pytest.mark.django_db
def test_create_milestone_invalid_title(get_token):
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': 'Neki title',
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Milestone.objects.count() == 0


@pytest.mark.django_db
def test_create_milestone_missing_description(get_token):
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': 'Milestone40',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Milestone.objects.count() == 0


@pytest.mark.django_db
def test_create_milestone_missing_repo(get_token):
    url = f'/milestone/create/{username}/nepostojeci_repo/'
    data = {
        'title': 'Milestone40',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Milestone.objects.count() == 0


@pytest.mark.django_db
def test_create_milestone_(get_token):
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': 'Milestone40',
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert Milestone.objects.count() == 1

    response2 = client.post(url, data, headers=headers)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert Milestone.objects.count() == 1


# UPDATE

@pytest.mark.django_db
def test_update_milestone_success(get_token):
    title = 'Milestone40'
    url_update = f'/milestone/update/{username}/{title}/'
    data_update = {
        'title': 'Milestone50',
        'description': 'Opis',
        'deadline': '2024-02-10',
        'repo_name': repo_name
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }

    # Create milestone
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': title,
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    response1 = client.post(url, data, headers=headers)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.data['title'] == 'Milestone40'

    # Update milestone
    response2 = client.patch(url_update, data_update, headers=headers)
    assert response2.status_code == status.HTTP_200_OK
    assert response2.data['title'] == 'Milestone50'
    assert Milestone.objects.count() == 1


@pytest.mark.django_db
def test_update_milestone_missing_repo(get_token):
    title = 'Milestone40'
    url_update = f'/milestone/update/{username}/{title}/'
    data_update = {
        'title': 'Milestone50',
        'description': 'Opis',
        'deadline': '2024-02-10',
        'repo_name': 'nepostojeci_repo'
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }

    # Create milestone
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': title,
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    response1 = client.post(url, data, headers=headers)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.data['title'] == 'Milestone40'

    # Update milestone
    response2 = client.patch(url_update, data_update, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Milestone.objects.count() == 1


@pytest.mark.django_db
def test_update_milestone_missing_milestone(get_token):
    title = 'Milestone40'
    url_update = f'/milestone/update/{username}/{title}/'
    data_update = {
        'title': 'Milestone50',
        'description': 'Opis',
        'deadline': '2024-02-10',
        'repo_name': repo_name
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }

    # Update milestone
    response2 = client.patch(url_update, data_update, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Milestone.objects.count() == 0


# DELETE

@pytest.mark.django_db
def test_delete_milestone_success(get_token):
    # CREATE MILESTONE
    title = 'Milestone40'
    url = f'/milestone/create/{username}/{repo_name}/'
    data = {
        'title': title,
        'description': 'Opis',
        'deadline': '2024-02-10',
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Milestone40'
    assert Milestone.objects.count() == 1

    # DELETE MILESTONE
    url_delete = f'/milestone/delete/{username}/{repo_name}/{title}/'
    response2 = client.delete(url_delete, headers=headers)
    assert response2.status_code == status.HTTP_204_NO_CONTENT
    assert Milestone.objects.count() == 0


@pytest.mark.django_db
def test_delete_milestone_missing_milestone(get_token):
    title = 'title'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    # DELETE MILESTONE
    url_delete = f'/milestone/delete/{username}/{repo_name}/{title}/'
    response2 = client.delete(url_delete, headers=headers)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
