import requests
from django.conf import settings

gitea_base_url = settings.GITEA_BASE_URL
access_token = settings.GITEA_ACCESS_TOKEN
admin_username = settings.GITEA_ADMIN_USERNAME
admin_pass = settings.GITEA_ADMIN_PASS

def save_user(user_data):
    api_endpoint = '/api/v1/admin/users'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=user_data)

def delete_user(username):
    api_endpoint = f'/api/v1/admin/users/{username}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    requests.delete(f'{gitea_base_url}{api_endpoint}', headers=headers)

def get_user_token(username):
    api_endpoint = f'/api/v1/users/{username}/tokens'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        'name': 'user_access_token_all',
        'scopes': [
            'read:activitypub', 'write:activitypub', 'read:issue', 'write:issue', 'read:misc', 'write:misc', 'read:notification', 'write:notification',
            'read:organization', 'write:organization', 'write:package', 'read:repository', 'write:repository', 'read:user', 'write:user'
        ]
    }
    response = requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data, auth=(admin_username, admin_pass))
    return response.json().get('sha1')

def get_user_avatar(user_token):
    api_endpoint = f'/api/v1/user'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {user_token}',
    }
    response = requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers)
    return response.json().get('avatar_url')

def create_repository(repo_data, username):
    api_endpoint = f'/api/v1/admin/users/{username}/repos'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=repo_data)

def get_root_content(username, repository, ref):
    api_endpoint = f'/api/v1/repos/{username}/{repository}/contents?ref={ref}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()

def get_folder_content(username, repository, branch, path):
    api_endpoint = f'/api/v1/repos/{username}/{repository}/contents/{path}?ref={branch}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()

def get_repository(owner, repository):
    api_endpoint = f'/api/v1/repos/{owner}/{repository}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    return requests.get(f'{gitea_base_url}{api_endpoint}', headers=headers).json()

def update_repository(owner, repository, old_name): 
    api_endpoint = f'/api/v1/repos/{owner}/{old_name}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        'name': repository.name,
        'description': repository.description,
        'private': repository.access_modifier == 'Private',
        'default_branch': repository.default_branch.name
    }
    requests.patch(f'{gitea_base_url}{api_endpoint}', headers=headers, json=data)

def delete_repository(owner, repository_name):
    api_endpoint = f'/api/v1/repos/{owner}/{repository_name}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    requests.delete(f'{gitea_base_url}{api_endpoint}', headers=headers)
