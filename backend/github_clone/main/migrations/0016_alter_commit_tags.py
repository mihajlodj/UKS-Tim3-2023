# Generated by Django 4.2.7 on 2024-01-30 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_pullrequest_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='commits', to='main.tag'),
        ),
    ]