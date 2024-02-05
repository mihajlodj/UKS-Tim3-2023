# Generated by Django 4.2.7 on 2024-02-05 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_branch_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='milestone',
            name='state',
            field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=10),
        ),
        migrations.AddField(
            model_name='milestone',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]