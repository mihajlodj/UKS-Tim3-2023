# Generated by Django 4.2.7 on 2024-01-30 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_commit_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Merged', 'Merged')], default='Open', max_length=10),
        ),
    ]
