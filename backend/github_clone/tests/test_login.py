import pytest
from django.contrib.auth.models import User
from main.models import RegistrationCandidate, Developer
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker


client = APIClient()
fake = Faker()
developer_email = 'fake.email@gmail.com'
developer_username = 'dev_username'
candidate_email = 'fake1.email@gmail.com'
candidate_username = 'candidate_username'
password = 'SomePassword123'


@pytest.fixture(autouse=True)
def create_developer():
    user = User(username=developer_username, email=developer_email, first_name=fake.first_name, last_name=fake.last_name, is_active=True)
    user.set_password(password)
    user.save()
    developer = Developer(user=user)
    developer.save()


@pytest.fixture(autouse=True)
def create_registration_candidate():
    user = User(username=candidate_username, email=candidate_email, first_name=fake.first_name, last_name=fake.last_name, is_active=False)
    user.set_password(password)
    user.save()
    candidate = RegistrationCandidate(user=user, code='123456')
    candidate.save()


@pytest.mark.django_db
def test_login_success():
    url = '/auth/login/'
    payload = {
        'username': developer_username,
        'password': password,
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    

@pytest.mark.django_db
def test_login_fail_incorrect_username():
    url = '/auth/login/'
    payload = {
        'username': 'WRONG',
        'password': password,
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'No active account found with the given credentials'


@pytest.mark.django_db
def test_login_fail_incorrect_password():
    url = '/auth/login/'
    payload = {
        'username': developer_username,
        'password': 'WRONG_PASS123',
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'No active account found with the given credentials'


@pytest.mark.django_db
def test_login_fail_try_as_registration_candidate():
    url = '/auth/login/'
    payload = {
        'username': candidate_username,
        'password': password,
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'No active account found with the given credentials'
