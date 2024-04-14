import threading
from main.models import Invitation, WorksOn, Role
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def invite_collaborator(developer, inviter_username, project):
    Invitation.objects.create(developer=developer, project=project)
    owner_username = WorksOn.objects.filter(role=Role.OWNER, project=project).first().developer.user.username
    threading.Thread(target=send_email, args=([developer, inviter_username, owner_username, project.name]), kwargs={}).start()


def send_email(invited_developer, inviter_username, owner_username, repository_name):
    subject = f'{inviter_username} invited you to {owner_username}/{repository_name}'
    template_vars = {
        'name': invited_developer.user.username,
        'inviter_username': inviter_username,
        'repository_name': f'{owner_username}/{repository_name}',
        'link_to_repo': f'http://localhost:3001/view/{owner_username}/{repository_name}',
        'link_to_owner': 'http://google.com',  # TODO
        'owner_username': owner_username,
        'link_to_invitation': 'http://google.com' # TODO
    }
    html_message = render_to_string('collaboration_invitation_email.html', template_vars)
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [invited_developer.user.email,]
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
