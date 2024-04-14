from main import gitea_service
from main.models import Developer


def get_dev_avatar(username):
    developer = Developer.objects.get(user__username=username)
    if developer.avatar is None:
        gitea_user_info = gitea_service.get_gitea_user_info_gitea_service(username)
        return gitea_user_info['avatar_url']
    avatar_filename = developer.avatar
    avatar_filename = avatar_filename.split('/')[1]
    avatar_url = 'http://localhost/avatars/git_profile_picture.png'
    if avatar_filename != '':
        avatar_url = f"http://localhost/avatars/{avatar_filename}"
    return avatar_url
