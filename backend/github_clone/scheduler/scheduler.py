from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from main.models import RegistrationCandidate, Invitation
from main.gitea_service import delete_user


def remove_registration_candidates():
    expiration_time = timezone.now() - timedelta(minutes=30)
    expired_candidates = RegistrationCandidate.objects.filter(created_at__lt=expiration_time)
    for candidate in expired_candidates:
        delete_user(candidate.user.username)
        candidate.user.delete()
        candidate.delete()


def remove_invitations():
    expiration_time = timezone.now() - timedelta(days=7)
    expired_invitations = Invitation.objects.filter(timestamp__lt=expiration_time)
    for invitation in expired_invitations:
        invitation.delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_job(remove_registration_candidates, 'interval', minutes=30, name='clean_accounts', jobstore='default')
    scheduler.add_job(remove_invitations, 'interval', hours=24, name='clear_invitations', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print('Scheduler started...')