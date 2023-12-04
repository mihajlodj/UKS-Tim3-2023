from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from main.models import RegistrationCandidate


def remove_registration_candidates():
    expiration_time = timezone.now() - timedelta(minutes=30)
    expired_candidates = RegistrationCandidate.objects.filter(created_at__lt=expiration_time)
    for candidate in expired_candidates:
        candidate.user.delete()
        candidate.delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_job(remove_registration_candidates, 'interval', minutes=30, name='clean_accounts', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print('Scheduler started...')