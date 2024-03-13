# Generated by Django 4.2.7 on 2024-02-17 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_pullrequest_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pullrequest',
            name='reviewers',
            field=models.ManyToManyField(blank=True, related_name='pull_requests_reviewers', to='main.developer'),
        ),
    ]
