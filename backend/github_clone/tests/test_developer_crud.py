# pytest --ds=github_clone.settings

import pytest
from django.contrib.auth.models import User
from main.models import Developer, SecondaryEmail
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'
username = 'MyUsername'
password = 'MyPassword123'
first_name = 'First'
last_name = 'Last'


@pytest.fixture(autouse=True)
def create_developer():
    user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name,
                               is_active=True)
    user.set_password(password)
    user.save()
    developer = Developer.objects.create(user=user)
    return developer


@pytest.fixture
def get_token(create_developer):
    url = '/auth/login/'
    payload = {
        'username': create_developer.user.username,
        'password': password,
    }
    response = client.post(url, payload)
    return response.data['access']


@pytest.mark.django_db
def test_update_user_info(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/update/{username}/'
    new_first_name = 'NewFirst'
    new_last_name = 'NewLast'
    new_username = 'NewUsername'

    user_data = {
        'first_name': new_first_name,
        'last_name': new_last_name,
        'username': new_username,
    }
    response = client.patch(url, user_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    assert response.data['first_name'] == new_first_name
    assert response.data['last_name'] == new_last_name
    assert response.data['username'] == new_username


@pytest.mark.django_db
def test_change_users_password(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/update/password/{username}/'
    new_password = 'NewPassword123'
    new_password_repeat = 'NewPassword123'

    password_data = {
        'current_password': password,
        'new_password': new_password,
        'new_password_repeat': new_password_repeat,
    }

    response = client.patch(url, password_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_user_info_invalid_username(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    invalid_username = 'NonExistentUser'
    url = f'/developer/update/{invalid_username}/'
    invalid_user_data = {
        'first_name': 'NewFirst',
        'last_name': 'NewLast',
        'username': 'NewUsername',
    }

    response = client.patch(url, invalid_user_data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_change_users_password_invalid_username(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    invalid_username = 'NonExistentUser'
    url = f'/developer/update/password/{invalid_username}/'

    new_password = 'NewPassword123'
    new_password_repeat = 'NewPassword123'

    invalid_password_data = {
        'current_password': password + "someSalt",
        'new_password': new_password,
        'new_password_repeat': new_password_repeat,
    }

    response = client.patch(url, invalid_password_data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_user_info_partial_update(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/update/{username}/'
    partial_user_data = {
        'first_name': 'UpdatedFirst',
    }

    response = client.patch(url, partial_user_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["first_name"] == 'UpdatedFirst'
    assert response.data["last_name"] == last_name
    assert response.data["username"] == username


@pytest.mark.django_db
def test_update_user_info_empty_fields(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/update/{username}/'
    empty_user_data = {
        'first_name': '',
        'last_name': '',
        'username': '',
    }

    response = client.patch(url, empty_user_data, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'This field may not be blank' in str(response.data)


@pytest.mark.django_db
def test_add_new_email(get_token,create_developer):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/newEmail/{username}/'
    new_email = 'new.email@example.com'

    email_data = {
        'secondary_emails': new_email
    }

    response = client.post(url, email_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    developer = Developer.objects.get(user_id=create_developer.user.id)
    assert developer.secondaryemail_set.filter(email=new_email).exists()


@pytest.mark.django_db
def test_delete_user_himself(get_token):
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/delete/self/{username}/{password}'

    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not User.objects.filter(username=username).exists()
    assert not Developer.objects.filter(user__username=username).exists()


@pytest.mark.django_db
def test_delete_developers_email(get_token,create_developer):
    usersEmail = 'delete.me@example.com'
    tempDeveloper = Developer.objects.get(user_id=create_developer.user.id)
    SecondaryEmail.objects.create(developer=tempDeveloper, email=usersEmail, primary=False, verified=True)
    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/delete/email/{username}/{usersEmail}'

    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    developer = Developer.objects.get(user__username=username)
    assert not developer.secondaryemail_set.filter(email=email).exists()


@pytest.mark.django_db
def test_get_developers_emails(get_token,create_developer):
    email1 = 'email1@example.com'
    email2 = 'email2@example.com'
    primery_email = 'fake.email@gmail.com'
    tempDeveloper = Developer.objects.get(user_id=create_developer.user.id)
    SecondaryEmail.objects.create(developer=tempDeveloper, email=email1, primary=False, verified=True)
    SecondaryEmail.objects.create(developer=tempDeveloper, email=email2, primary=False, verified=False)

    headers = {
        'Authorization': f'Bearer {get_token}'
    }
    url = f'/developer/emails/{username}/'

    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    assert primery_email in str(response.data[0])
    assert email1 in str(response.data[2])
    assert email2 in str(response.data[1])
