# Generated by Django 4.2.7 on 2024-02-07 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workson',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Unregistered', 'Unregistered'), ('Readonly', 'Readonly'), ('Developer', 'Developer'), ('Maintainer', 'Maintainer'), ('Owner', 'Owner'), ('IsBanned', 'IsBanned')], default='Developer', max_length=20),
        ),
    ]