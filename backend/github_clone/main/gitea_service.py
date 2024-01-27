import requests
from django.conf import settings

gitea_base_url = settings.GITEA_BASE_URL
access_token = settings.GITEA_ACCESS_TOKEN

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

def create_repository(repo_data, username):
    api_endpoint = f'/api/v1/admin/users/{username}/repos'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    requests.post(f'{gitea_base_url}{api_endpoint}', headers=headers, json=repo_data)

