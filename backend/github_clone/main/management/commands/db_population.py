from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def _make_suepruser(self):
        users = User.objects.all()
        if len(users) == 0:
            User.objects.create_superuser("admin", "admin@admin.admin", "admin")

    def handle(self, *args, **options):
        self._make_suepruser()
