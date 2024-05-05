# Generated by Django 4.2.7 on 2024-05-04 17:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_issue_created_pullrequestassignee'),
    ]

    operations = [
        migrations.CreateModel(
            name='PullRequestReviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pull_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pull_request', to='main.pullrequest')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to='main.developer')),
            ],
        ),
        migrations.AlterField(
            model_name='issue',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 4, 17, 45, 55, 205944, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='PullRequestAssignee',
        ),
    ]