# Generated by Django 4.2.7 on 2024-02-18 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_issue_created_issue_open_issue_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 18, 12, 34, 26, 442777, tzinfo=datetime.timezone.utc)),
        ),
    ]