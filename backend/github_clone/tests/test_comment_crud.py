import pytest
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch, Milestone, MilestoneState, Event, Comment
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from datetime import datetime
from main import gitea_service

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username = 'MyUsername'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
milestone_title = 'Milestone1'

comment_content = 'Comment content'


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
def disable_gitea_create_milestone(monkeypatch):
    def mock_create_milestone(*args, **kwargs):
        return 2
    monkeypatch.setattr(gitea_service, 'create_milestone', mock_create_milestone)
    yield


@pytest.fixture(autouse=True)
def save_milestone(create_developer):
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')

    current_datetime = datetime.now()
    current_datetime_formatted = current_datetime.strftime('%Y-%m-%d')
    # Event.objects.create()
    milestone = Milestone.objects.create(title=milestone_title,
                                         description=fake.text,
                                         state=MilestoneState.OPEN,
                                         deadline=current_datetime_formatted,
                                         project=repo)
    milestone.save()

# CREATE


@pytest.mark.django_db
def test_create_comment_success(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "parent": "",
        "type_for": "milestone",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['content'] == comment_content
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_create_comment_missing_content(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "parent": "",
        "type_for": "milestone",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_create_comment_missing_parent(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "type_for": "milestone",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_create_comment_content_blank(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": '',
        "parent": "",
        "type_for": "milestone",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_create_comment_type_for_blank(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "parent": "",
        "type_for": "",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_create_comment_type_id_blank(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "parent": "",
        "type_for": "milestone",
        "type_id": ''
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_create_comment_unauthorized(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "parent": "",
        "type_for": "milestone",
        "type_id": milestone.id
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_create_comment_type_for_invalid(get_token):
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "parent": "",
        "type_for": "invalid",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Comment.objects.count() == 0


# DELETE

@pytest.mark.django_db
def test_delete_comment_success(get_token):
    # Create Comment
    milestone = Milestone.objects.get(title=milestone_title)

    url = '/comment/create/'
    data = {
        "content": comment_content,
        "parent": "",
        "type_for": "milestone",
        "type_id": milestone.id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['content'] == comment_content
    assert Comment.objects.count() == 1

    comment = Comment.objects.get(content=comment_content)

    url_delete = f'/comment/delete/{comment.id}/'
    response2 = client.delete(url_delete, headers=headers)
    assert response2.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_delete_comment_comment_id_empty(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url_delete = f'/comment/delete/'
    response2 = client.delete(url_delete, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_delete_comment_comment_id_not_digit(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url_delete = f'/comment/delete/aaa/'
    response2 = client.delete(url_delete, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_delete_comment_comment_doesnt_exist(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url_delete = f'/comment/delete/1/'
    assert Comment.objects.count() == 0
    response2 = client.delete(url_delete, headers=headers)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert Comment.objects.count() == 0
