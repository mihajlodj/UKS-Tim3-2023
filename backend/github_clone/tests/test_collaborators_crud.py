import json
import pytest
from django.contrib.auth.models import User
from main.models import Developer, Invitation, Project, Role, WorksOn, Branch
from rest_framework.test import APIClient
from rest_framework import status
from faker import Faker
from main import gitea_service
from repository import service

client = APIClient()
fake = Faker()
email = 'fake.email@gmail.com'

username_owner = 'MyUsername'
username_maintainer = 'MyUsername2'
username_non_member = 'NotMember'
username_developer = 'DeveloperUsername'
username_readonly = 'ReadonlyUsername'

password = 'MyPassword123'

repo_name = 'MyNewTestRepo'


@pytest.fixture
def create_developers():
    user_owner = User.objects.create_user(username=username_owner, password=password)
    owner = Developer.objects.create(user=user_owner)
    user_maintainer = User.objects.create_user(username=username_maintainer, password=password)
    maintainer = Developer.objects.create(user=user_maintainer)
    user_developer = User.objects.create_user(username=username_developer, password=password)
    developer = Developer.objects.create(user=user_developer)
    user_readonly = User.objects.create_user(username=username_readonly, password=password)
    readonly = Developer.objects.create(user=user_readonly)
    return owner, maintainer, developer, readonly


@pytest.fixture
def create_developer():
    user = User.objects.create_user(username=username_non_member, password=password)
    return Developer.objects.create(user=user)
    

@pytest.fixture
def create_invitation(create_developer, create_repository):
    return Invitation.objects.create(developer=create_developer, project=create_repository, role=Role.MAINTAINER)


@pytest.fixture
def get_token_as_owner(create_developers):
    payload = {
        'username': create_developers[0].user.username,
        'password': password,
    }
    return client.post('/auth/login/', payload).data['access']


@pytest.fixture
def get_token_as_maintainer(create_developers):
    payload = {
        'username': create_developers[1].user.username,
        'password': password,
    }
    return client.post('/auth/login/', payload).data['access']


@pytest.fixture
def get_token_as_developer(create_developers):
    payload = {
        'username': create_developers[2].user.username,
        'password': password,
    }
    return client.post('/auth/login/', payload).data['access']


@pytest.fixture
def get_token_as_readonly(create_developers):
    payload = {
        'username': create_developers[3].user.username,
        'password': password,
    }
    return client.post('/auth/login/', payload).data['access']


@pytest.fixture
def get_token_as_non_member(create_developer):
    payload = {
        'username': create_developer.user.username,
        'password': password,
    }
    return client.post('/auth/login/', payload).data['access']


@pytest.fixture(autouse=True)
def create_repository(create_developers):
    owner, maintainer, developer, readonly = create_developers
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')
    main = Branch.objects.create(name='main', project=repo, created_by=owner)
    repo.default_branch = main
    repo.save()
    WorksOn.objects.create(role=Role.OWNER, project=repo, developer=owner)
    WorksOn.objects.create(role=Role.MAINTAINER, project=repo, developer=maintainer)
    WorksOn.objects.create(role=Role.DEVELOPER, project=repo, developer=developer)
    WorksOn.objects.create(role=Role.READONLY, project=repo, developer=readonly)
    return repo


@pytest.fixture(autouse=True)
def disable_get_gitea_user_info_gitea_service(monkeypatch):
    def mock_get_gitea_user_info_gitea_service(*args, **kwargs):
        return {'username': 'abc', 'avatar': 'avatar', 'email': 'email'}
    monkeypatch.setattr(gitea_service, 'get_gitea_user_info_gitea_service', mock_get_gitea_user_info_gitea_service)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_add_collaborator(monkeypatch):
    def mock_add_collaborator(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'add_collaborator', mock_add_collaborator)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_delete_collaborator(monkeypatch):
    def mock_delete_collaborator(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'delete_collaborator', mock_delete_collaborator)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_change_collaborator_role(monkeypatch):
    def mock_change_collaborator_role(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'change_collaborator_role', mock_change_collaborator_role)
    yield


@pytest.fixture(autouse=True)
def disable_gitea_transfer_ownership(monkeypatch):
    def mock_transfer_ownership(*args, **kwargs):
        return
    monkeypatch.setattr(gitea_service, 'transfer_ownership', mock_transfer_ownership)
    yield


@pytest.fixture(autouse=True)
def disable_send_email(monkeypatch):
    def mock_send_email(*args, **kwargs):
        return
    monkeypatch.setattr(service, 'send_email', mock_send_email)


@pytest.mark.django_db
def test_invite_collaborator_success(get_token_as_owner, create_developer):
    dev = create_developer
    url = f'/repository/invite/{username_owner}/{repo_name}/{dev.user.username}/'
    payload = {'role': 'Maintainer'}
    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == username_non_member
    assert response.data['role'] == 'Pending'
    assert Invitation.objects.count() == 1
    assert Invitation.objects.filter().first().role == Role.MAINTAINER


@pytest.mark.django_db
def test_invite_collaborator_already_added(get_token_as_owner):
    url = f'/repository/invite/{username_owner}/{repo_name}/{username_maintainer}/'
    payload = {'role': 'Developer'}
    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Invitation.objects.count() == 0


@pytest.mark.django_db
def test_invite_collaborator_as_maintainer_success(get_token_as_maintainer, create_developer):
    dev = create_developer
    url = f'/repository/invite/{username_owner}/{repo_name}/{dev.user.username}/'
    payload = {'role': 'Developer'}
    headers = { 'Authorization': f'Bearer {get_token_as_maintainer}' }
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == username_non_member
    assert response.data['role'] == 'Pending'
    assert Invitation.objects.count() == 1
    assert Invitation.objects.filter().first().role == Role.DEVELOPER


@pytest.mark.django_db
def test_invite_collaborator_as_developer(get_token_as_developer, create_developer):
    dev = create_developer
    url = f'/repository/invite/{username_owner}/{repo_name}/{dev.user.username}/'
    payload = {'role': 'Developer'}
    headers = { 'Authorization': f'Bearer {get_token_as_developer}' }
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Invitation.objects.count() == 0


@pytest.mark.django_db
def test_invite_collaborator_as_readonly(get_token_as_readonly, create_developer):
    dev = create_developer
    url = f'/repository/invite/{username_owner}/{repo_name}/{dev.user.username}/'
    payload = {'role': 'Developer'}
    headers = { 'Authorization': f'Bearer {get_token_as_readonly}' }
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Invitation.objects.count() == 0


@pytest.mark.django_db
def test_accept_invitation_success(get_token_as_non_member, create_invitation):
    invitation = create_invitation
    assert Invitation.objects.filter(id=invitation.id).count() == 1
    assert WorksOn.objects.filter(project=invitation.project, developer=invitation.developer).count() == 0
    url = f'/repository/inviteResponse/{username_owner}/{repo_name}/{username_non_member}/accept/'
    headers = { 'Authorization': f'Bearer {get_token_as_non_member}' }
    response = client.post(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Invitation.objects.count() == 0
    assert WorksOn.objects.filter(project=invitation.project, developer=invitation.developer).count() == 1
    assert WorksOn.objects.filter(project=invitation.project, developer=invitation.developer).first().role == Role.MAINTAINER


@pytest.mark.django_db
def test_decline_invitation_success(get_token_as_non_member, create_invitation):
    invitation = create_invitation
    assert Invitation.objects.filter(id=invitation.id).count() == 1
    assert WorksOn.objects.filter(project=invitation.project, developer=invitation.developer).count() == 0
    url = f'/repository/inviteResponse/{username_owner}/{repo_name}/{username_non_member}/decline/'
    headers = { 'Authorization': f'Bearer {get_token_as_non_member}' }
    response = client.post(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert Invitation.objects.count() == 0
    assert WorksOn.objects.filter(project=invitation.project, developer=invitation.developer).count() == 0


@pytest.mark.django_db
def test_accept_invitation_not_invited(get_token_as_non_member, create_developer, create_repository):
    assert Invitation.objects.count() == 0
    assert WorksOn.objects.filter(project=create_repository, developer=create_developer).count() == 0
    url = f'/repository/inviteResponse/{username_owner}/{repo_name}/{username_non_member}/accept/'
    headers = { 'Authorization': f'Bearer {get_token_as_non_member}' }
    response = client.post(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Invitation.objects.count() == 0
    assert WorksOn.objects.filter(project=create_repository, developer=create_developer).count() == 0


@pytest.mark.django_db
def test_accept_invitation_not_invited(get_token_as_non_member, create_developer, create_repository):
    assert Invitation.objects.count() == 0
    assert WorksOn.objects.filter(project=create_repository, developer=create_developer).count() == 0
    url = f'/repository/inviteResponse/{username_owner}/{repo_name}/{username_non_member}/decline/'
    headers = { 'Authorization': f'Bearer {get_token_as_non_member}' }
    response = client.post(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Invitation.objects.count() == 0
    assert WorksOn.objects.filter(project=create_repository, developer=create_developer).count() == 0


@pytest.mark.django_db
def test_remove_collaborator_success_except_for_owner(get_token_as_owner, get_token_as_maintainer, create_developers, create_repository, create_invitation):
    owner, maintainer, developer, readonly = create_developers
    assert WorksOn.objects.filter(project=create_repository, developer=maintainer).count() == 1
    assert WorksOn.objects.filter(project=create_repository, developer=developer).count() == 1
    assert WorksOn.objects.filter(project=create_repository, developer=readonly).count() == 1
    assert Invitation.objects.filter(id=create_invitation.id).count() == 1

    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    
    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_maintainer}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert WorksOn.objects.filter(project=create_repository, developer=maintainer).count() == 0

    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_developer}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert WorksOn.objects.filter(project=create_repository, developer=developer).count() == 0

    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_readonly}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert WorksOn.objects.filter(project=create_repository, developer=readonly).count() == 0

    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_non_member}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Invitation.objects.filter(id=create_invitation.id).count() == 0

    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_owner}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert WorksOn.objects.filter(project=create_repository, developer=owner).count() == 1


@pytest.mark.django_db
def test_remove_collaborator_cannot_for_self(get_token_as_maintainer, create_developers, create_repository, create_invitation):
    owner, maintainer, developer, readonly = create_developers
    assert WorksOn.objects.filter(project=create_repository, developer=maintainer).count() == 1
    assert WorksOn.objects.filter(project=create_repository, developer=developer).count() == 1
    assert WorksOn.objects.filter(project=create_repository, developer=readonly).count() == 1
    assert WorksOn.objects.filter(project=create_repository, developer=owner).count() == 1
    assert Invitation.objects.filter(id=create_invitation.id).count() == 1

    headers = { 'Authorization': f'Bearer {get_token_as_maintainer}' }
    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_maintainer}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert WorksOn.objects.filter(project=create_repository, developer=maintainer).count() == 1


@pytest.mark.django_db
def test_remove_does_not_exist(get_token_as_owner):
    assert WorksOn.objects.filter(developer__user__username=username_non_member).count() == 0

    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    url = f'/repository/removeCollaborator/{username_owner}/{repo_name}/{username_non_member}'
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_change_role_success(get_token_as_owner, create_repository):
    repo = create_repository
    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()
    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    payload = {'role': Role.DEVELOPER}
    url = f'/repository/editRole/{username_owner}/{repo_name}/{username_maintainer}/'
    response = client.put(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert not WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.DEVELOPER).exists()


@pytest.mark.django_db
def test_change_role_invalid_role_owner(get_token_as_owner, create_repository):
    repo = create_repository
    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()
    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    payload = {'role': Role.OWNER}
    url = f'/repository/editRole/{username_owner}/{repo_name}/{username_maintainer}/'
    response = client.put(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == 'Invalid role'
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()

@pytest.mark.django_db
def test_change_role_invalid_role_owner(get_token_as_owner, create_repository):
    repo = create_repository
    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()
    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    payload = {'role': Role.ADMIN}
    url = f'/repository/editRole/{username_owner}/{repo_name}/{username_maintainer}/'
    response = client.put(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == 'Invalid role'
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()

@pytest.mark.django_db
def test_change_role_invalid_role_owner(get_token_as_owner, create_repository):
    repo = create_repository
    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()
    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    payload = {'role': Role.IS_BANNED}
    url = f'/repository/editRole/{username_owner}/{repo_name}/{username_maintainer}/'
    response = client.put(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == 'Invalid role'
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()


@pytest.mark.django_db
def test_transfer_ownership_success(get_token_as_owner, create_repository):
    repo = create_repository
    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()

    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    payload = { 'new_owner': username_maintainer }
    url = f'/repository/transfer/{username_owner}/{repo_name}/'
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_200_OK

    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.MAINTAINER).exists()
    assert not WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert not WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.MAINTAINER).exists()
    assert WorksOn.objects.filter(developer__user__username=username_maintainer, project=repo, role=Role.OWNER).exists()


@pytest.mark.django_db
def test_transfer_ownership_collaborator_does_not_exist(get_token_as_owner, create_repository):
    repo = create_repository
    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert not WorksOn.objects.filter(developer__user__username=username_non_member, project=repo).exists()

    headers = { 'Authorization': f'Bearer {get_token_as_owner}' }
    payload = { 'new_owner': username_non_member }
    url = f'/repository/transfer/{username_owner}/{repo_name}/'
    response = client.post(url, content_type='application/json', data=json.dumps(payload), headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert WorksOn.objects.filter(developer__user__username=username_owner, project=repo, role=Role.OWNER).exists()
    assert not WorksOn.objects.filter(developer__user__username=username_non_member, project=repo, role=Role.OWNER).exists()
