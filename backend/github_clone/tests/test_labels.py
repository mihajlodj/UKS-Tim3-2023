import pytest
from unittest.mock import patch
from django.contrib.auth.models import User
from main.models import Developer, Project, WorksOn, Branch, Milestone, Label
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from main import gitea_service

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username = 'MyUsername'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
repo_name2 = 'MyNewTestRepo2'
label_name = 'feature_label1'
empty_description = ''
description = 'Some label description'


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


# Create

@pytest.mark.django_db
def test_create_label_success(get_token):
    url = f'/label/create/{username}/{repo_name}/'
    data = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == label_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1


@pytest.mark.django_db
def test_create_label_missing_name(get_token):
    url = f'/label/create/{username}/{repo_name}/'
    data = {
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_create_label_missing_description(get_token):
    url = f'/label/create/{username}/{repo_name}/'
    data = {
        "name": label_name,
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_create_label_name_blank(get_token):
    url = f'/label/create/{username}/{repo_name}/'
    data = {
        "name": '',
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_create_label_project_name_not_valid(get_token):
    url = f'/label/create/{username}//'
    data = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_create_label_project_doesnt_exist(get_token):
    repo_doesnt_exist_name = 'rem'
    url = f'/label/create/{repo_doesnt_exist_name}/'
    data = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_create_label_name_is_duplicate(get_token):
    # Create first Label
    url = f'/label/create/{username}/{repo_name}/'
    data = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == label_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1
    # Create second label
    response2 = client.post(url, data, headers=headers)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert Label.objects.count() == 1


@pytest.mark.django_db
def test_create_label_no_token_sent(get_token):
    url = f'/label/create/{username}/{repo_name}/'
    data = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Label.objects.count() == 0


# Update

@pytest.mark.django_db
def test_update_label_success(get_token):
    # Create label
    url1 = f'/label/create/{username}/{repo_name}/'
    data1 = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url1, data1, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == label_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1

    # Update label
    label = Label.objects.get(name=label_name)
    label_id = label.id
    new_name = 'new label name'

    url2 = f'/label/update/{username}/{repo_name}/{label_id}/'
    data2 = {
        "name": new_name,
        "description": empty_description
    }
    response = client.patch(url2, data2, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == new_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1


@pytest.mark.django_db
def test_update_label_label_id_is_none(get_token):
    # Update label
    label_id = ''
    new_name = 'new label name'

    url2 = f'/label/update/{username}/{repo_name}/{label_id}/'
    data2 = {
        "name": new_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.patch(url2, data2, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_update_label_label_id_is_not_digit(get_token):
    # Update label
    label_id = 'asdf'
    new_name = 'new label name'

    url2 = f'/label/update/{username}/{repo_name}/{label_id}/'
    data2 = {
        "name": new_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.patch(url2, data2, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_update_label_new_name_is_duplicate(get_token):
    # Create label
    url1 = f'/label/create/{username}/{repo_name}/'
    data1 = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url1, data1, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == label_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1

    # Update label
    label = Label.objects.get(name=label_name)
    label_id = label.id

    url2 = f'/label/update/{username}/{repo_name}/{label_id}/'
    data2 = {
        "name": label_name,
        "description": empty_description
    }
    response = client.patch(url2, data2, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == label_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1


# Delete


@pytest.mark.django_db
def test_delete_label_success(get_token):
    # Create label
    url1 = f'/label/create/{username}/{repo_name}/'
    data1 = {
        "name": label_name,
        "description": empty_description
    }
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.post(url1, data1, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == label_name
    assert response.data['description'] == empty_description
    assert Label.objects.count() == 1

    # Delete label
    label = Label.objects.get(name=label_name)
    label_id = label.id

    url2 = f'/label/delete/{username}/{repo_name}/{label_id}/'
    response = client.delete(url2, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Label.objects.count() == 0


@pytest.mark.django_db
def test_delete_label_label_id_is_not_digit(get_token):
    label_id = 'asdf'

    url2 = f'/label/delete/{username}/{repo_name}/{label_id}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url2, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_label_label_doesnt_exist(get_token):
    label_id = 10

    url2 = f'/label/delete/{username}/{repo_name}/{label_id}/'
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    response = client.delete(url2, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
