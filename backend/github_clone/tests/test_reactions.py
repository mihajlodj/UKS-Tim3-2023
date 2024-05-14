import pytest
from unittest.mock import patch
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch, Milestone, MilestoneState, Event, Comment, Reaction
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

    developer = create_developer
    WorksOn.objects.create(role='Owner', project=repo, developer=developer)

    comment = Comment.objects.create(content=comment_content,
                                     parent=None,
                                     caused_by=developer)
    comment.milestone = milestone
    comment.save()


# Create


@pytest.mark.django_db
def test_create_reaction_success(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['code'] == code
    assert response.data['developer_id'] == developer_id
    assert response.data['comment_id'] == comment_id
    assert Reaction.objects.count() == 1


@pytest.mark.django_db
def test_create_reaction_missing_code(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_missing_developer_id(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_missing_comment_id(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_code_blank(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": '',
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_developer_id_blank(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": '',
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_comment_id_blank(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": ''
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_developer_doesnt_exist(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = "10"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_comment_doesnt_exist(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = "10"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_create_reaction_duplicate_reaction(get_token):
    url = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['code'] == code
    assert response.data['developer_id'] == developer_id
    assert response.data['comment_id'] == comment_id
    assert Reaction.objects.count() == 1

    response2 = client.post(url, data, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Reaction.objects.count() == 1


# Delete


@pytest.mark.django_db
def test_delete_reaction_success(get_token):
    url1 = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response1 = client.post(url1, data, headers=headers)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.data['code'] == code
    assert response1.data['developer_id'] == developer_id
    assert response1.data['comment_id'] == comment_id
    assert Reaction.objects.count() == 1

    created_reaction = Reaction.objects.get()
    created_reaction_id = created_reaction.id

    # Delete reaction
    url2 = f'/reaction/delete/{username}/{repo_name}/{created_reaction_id}/'
    response2 = client.delete(url2, headers=headers)
    assert response2.status_code == status.HTTP_204_NO_CONTENT
    assert Reaction.objects.count() == 0


@pytest.mark.django_db
def test_delete_reaction_reaction_id_is_not_digit(get_token):
    url1 = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response1 = client.post(url1, data, headers=headers)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.data['code'] == code
    assert response1.data['developer_id'] == developer_id
    assert response1.data['comment_id'] == comment_id
    assert Reaction.objects.count() == 1

    created_reaction = Reaction.objects.get()
    created_reaction_id = 'asdf'

    # Delete reaction
    url2 = f'/reaction/delete/{username}/{repo_name}/{created_reaction_id}/'
    response2 = client.delete(url2, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Reaction.objects.count() == 1


@pytest.mark.django_db
def test_delete_reaction_reaction_doesnt_exist(get_token):
    url1 = f'/reaction/create/{username}/{repo_name}/'
    developer = Developer.objects.get()
    comment = Comment.objects.get()

    code = r"\uD83C\uDF89"   # \uD83C\uDF89
    developer_id = f"{developer.id}"
    comment_id = f"{comment.id}"

    data = {
        "code": code,
        "developer_id": developer_id,
        "comment_id": comment_id
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response1 = client.post(url1, data, headers=headers)
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.data['code'] == code
    assert response1.data['developer_id'] == developer_id
    assert response1.data['comment_id'] == comment_id
    assert Reaction.objects.count() == 1

    created_reaction = Reaction.objects.get()
    created_reaction_id = 10

    # Delete reaction
    url2 = f'/reaction/delete/{username}/{repo_name}/{created_reaction_id}/'
    response2 = client.delete(url2, headers=headers)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert Reaction.objects.count() == 1

