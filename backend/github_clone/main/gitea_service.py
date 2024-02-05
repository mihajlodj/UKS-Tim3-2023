import requests
from django.conf import settings

gitea_base_url = settings.GITEA_BASE_URL
access_token = settings.GITEA_ACCESS_TOKEN
admin_username = settings.GITEA_ADMIN_USERNAME
admin_pass = settings.GITEA_ADMIN_PASS

headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }


def save_user(user_data):
    api_endpoint = '/api/v1/admin/users'
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=user_data)


def delete_user(username):
    api_endpoint = f'/api/v1/admin/users/{username}'
    requests.delete(f'{gitea_base_url}{api_endpoint}', headers=headers)


def get_user_token(username):
    api_endpoint = f'/api/v1/users/{username}/tokens'
    data = {
        'name': 'user_access_token_all',
        'scopes': [
            'read:activitypub', 'write:activitypub', 'read:issue', 'write:issue', 'read:misc', 'write:misc',
            'read:notification', 'write:notification',
            'read:organization', 'write:organization', 'write:package', 'read:repository', 'write:repository',
            'read:user', 'write:user'
        ]
    }
    response = requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data,
                             auth=(admin_username, admin_pass))
    return response.json().get('sha1')


def get_user_avatar(username):
    api_endpoint = f'/api/v1/users/{username}'
    response = requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers)
    return response.json().get('avatar_url')

def create_repository(repo_data, username):
    api_endpoint = f'/api/v1/admin/users/{username}/repos'
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=repo_data)


def get_root_content(username, repository, ref):
    api_endpoint = f'/api/v1/repos/{username}/{repository}/contents?ref={ref}'
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()


def get_folder_content(username, repository, branch, path):
    api_endpoint = f'/api/v1/repos/{username}/{repository}/contents/{path}?ref={branch}'
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()


def get_repository(owner, repository):
    api_endpoint = f'/api/v1/repos/{owner}/{repository}'
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()


def update_repository(owner, repository, old_name):
    api_endpoint = f'/api/v1/repos/{owner}/{old_name}'
    data = {
        'name': repository.name,
        'description': repository.description,
        'private': repository.access_modifier == 'Private',
        'default_branch': repository.default_branch.name
    }
    requests.patch(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data)


def delete_repository(owner, repository_name):
    api_endpoint = f'/api/v1/repos/{owner}/{repository_name}'
    requests.delete(f'{gitea_base_url}{api_endpoint}', headers=headers)


# user crud
def update_developer_username(new_username, old_username):
    api_endpoint = f'/api/v1/admin/users/{old_username}/rename'
    data = {
        'new_username': new_username,
    }
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data)


def get_gitea_user_info_gitea_service(username):
    api_endpoint = f'/api/v1/users/{username}'
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()


def get_gitea_user_emails_gitea_service():
    api_endpoint = f'/api/v1/admin/emails'
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()


def update_developer_info(new_username, new_first_name, new_last_name):
    api_endpoint = f'/api/v1/admin/users/{new_username}'
    data = {
        'full_name': new_first_name + " " + new_last_name,
    }
    return requests.patch(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data)


def change_gitea_user_password_gitea_service(username, new_password):
    api_endpoint = f'/api/v1/admin/users/{username}'
    data = {
        'password': new_password,
    }
    return requests.patch(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data)


def delete_gitea_user_gitea_service(username):
    print(username," je proslijedjeni")
    api_endpoint = f'/api/v1/admin/users/{username}'
    return requests.delete(f'{gitea_base_url}{api_endpoint}', headers=headers)

def create_branch(owner, repository_name, branch):
    api_endpoint = f'/api/v1/repos/{owner}/{repository_name}/branches'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        'new_branch_name': branch.name,
        'old_ref_name': branch.parent.name
    }
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data)

def delete_branch(owner, repository_name, branch_name):
    api_endpoint = f'/api/v1/repos/{owner}/{repository_name}/branches/{branch_name}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    requests.delete(f'{gitea_base_url}{api_endpoint}', headers=headers)
