# Generated by Django 4.2.7 on 2023-12-04 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_registrationcandidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationcandidate',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]