# pytest --ds=github_clone.settings

import pytest
from django.contrib.auth.models import User
from main.models import RegistrationCandidate
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from auth.serializers import RegistrationSerializer

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'

@pytest.fixture(autouse=True)
def disable_send_email(monkeypatch):
    def mock_send_email(*args, **kwargs):
        pass
    monkeypatch.setattr(RegistrationSerializer, 'send_email', mock_send_email)
    yield


@pytest.mark.django_db
def test_register_candidate_success():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1


@pytest.mark.django_db
def test_register_candidate_empty_username():
    url = '/auth/register/'
    payload = {
        'username': '',
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_register_candidate_empty_password():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': '',
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0
    
    
@pytest.mark.django_db
def test_register_candidate_empty_first_name():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': fake.password,
        'first_name': '',
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_register_candidate_empty_last_name():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': '',
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_register_candidate_empty_email():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': ''
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_register_candidate_duplicate_username():
    url = '/auth/register/'
    username = fake.user_name
    payload1 = {
        'username': username,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload1)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1
    payload2 = {
        'username': username,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': 'fake.email+1@gmail.com'
    }
    response = client.post(url, payload2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1


@pytest.mark.django_db
def test_register_candidate_duplicate_email():
    url = '/auth/register/'
    payload1 = {
        'username': fake.user_name,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload1)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1
    payload2 = {
        'username': fake.user_name,
        'password': fake.password,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1


@pytest.mark.django_db
def test_register_candidate_weak_password1():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': '123456',
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_register_candidate_weak_password2():
    url = '/auth/register/'
    payload = {
        'username': fake.user_name,
        'password': 'asnfejv',
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'email': email
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_confirm_registration_success():
    username = 'abcd'
    code = '123456'
    user = User.objects.create_user(username=username, first_name=fake.first_name, last_name=fake.last_name, email=email, password='MyPass123')
    user.save()
    assert User.objects.count() == 1
    candidate = RegistrationCandidate.objects.create(user=user, code=code)
    candidate.save()
    assert RegistrationCandidate.objects.count() == 1

    url = '/auth/register-confirm/'
    payload = {
        'username': username, 
        'code': code
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 0


@pytest.mark.django_db
def test_confirm_registration_wrong_username():
    username = 'abcd'
    code = '123456'
    user = User.objects.create_user(username=username, first_name=fake.first_name, last_name=fake.last_name, email=email, password='MyPass123')
    user.save()
    assert User.objects.count() == 1
    candidate = RegistrationCandidate.objects.create(user=user, code=code)
    candidate.save()
    assert RegistrationCandidate.objects.count() == 1

    url = '/auth/register-confirm/'
    payload = {
        'username': 'otherUsername', 
        'code': code
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1


@pytest.mark.django_db
def test_confirm_registration_wrong_code():
    username = 'abcd'
    code = '123456'
    user = User.objects.create_user(username=username, first_name=fake.first_name, last_name=fake.last_name, email=email, password='MyPass123')
    user.save()
    assert User.objects.count() == 1
    candidate = RegistrationCandidate.objects.create(user=user, code=code)
    candidate.save()
    assert RegistrationCandidate.objects.count() == 1

    url = '/auth/register-confirm/'
    payload = {
        'username': username, 
        'code': '111111'
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert User.objects.count() == 1
    assert RegistrationCandidate.objects.count() == 1
