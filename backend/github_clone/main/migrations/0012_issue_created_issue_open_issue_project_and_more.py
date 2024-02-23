# Generated by Django 4.2.7 on 2024-02-23 17:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_pullrequest_merged_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 23, 17, 1, 35, 582827, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='issue',
            name='open',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='project_issues', to='main.project'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='main.milestone'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]