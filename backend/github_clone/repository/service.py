import threading
from main.models import Branch, Commit, Developer, Fork, Invitation, Project, WorksOn, Role
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from main import gitea_service


def invite_collaborator(developer, inviter_username, project, role):
    Invitation.objects.create(developer=developer, project=project, role=role)
    owner_username = WorksOn.objects.filter(role=Role.OWNER, project=project).first().developer.user.username
    threading.Thread(target=send_email, args=([developer, inviter_username, owner_username, project.name]), kwargs={}).start()


def fork(original_repository: Project, new_repository_info, original_owner_username: str, new_owner: Developer):
    new_repository = Project.objects.create(name=new_repository_info['name'], description=new_repository_info['description'],
                                            access_modifier=original_repository.access_modifier)
    WorksOn.objects.create(developer=new_owner, project=new_repository, role=Role.OWNER)

    branches = Branch.objects.filter(project=original_repository)
    for branch in branches:
        new_branch = Branch.objects.create(name=branch.name, project=new_repository, created_by=branch.created_by)
        if original_repository.default_branch == branch:
            new_repository.default_branch = new_branch
        branch_commits = Commit.objects.filter(branch=branch)
        for commit in branch_commits:
            Commit.objects.create(hash=commit.hash, branch=new_branch, message=commit.message, author=commit.author, committer=commit.committer,
                                  timestamp=commit.timestamp, additional_description=commit.additional_description)
    new_repository.save()
    Fork.objects.create(developer=new_owner, source=original_repository, destination=new_repository)
    gitea_service.fork(original_owner_username, original_repository.name, new_owner.user.username, new_repository.name)        



def send_email(invited_developer, inviter_username, owner_username, repository_name):
    subject = f'{inviter_username} invited you to {owner_username}/{repository_name}'
    template_vars = {
        'name': invited_developer.user.username,
        'inviter_username': inviter_username,
        'repository_name': f'{owner_username}/{repository_name}',
        'link_to_repo': f'{settings.ACTIVE_ORIGIN}/view/{owner_username}/{repository_name}',
        'link_to_owner': f'{settings.ACTIVE_ORIGIN}/profile/{inviter_username}',
        'owner_username': owner_username,
        'link_to_invitation': f'{settings.ACTIVE_ORIGIN}/view/{owner_username}/{repository_name}/invitations/{invited_developer.user.username}'
    }
    html_message = render_to_string('collaboration_invitation_email.html', template_vars)
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [invited_developer.user.email,]
    send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
