# Generated by Django 4.2.7 on 2024-05-11 01:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_pullrequestreviewer_alter_issue_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 11, 1, 40, 6, 133611, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('pre_release', models.BooleanField(default=False)),
                ('draft', models.BooleanField(default=False)),
                ('commitish', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_release', to='main.project')),
                ('tag', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.tag')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='released_branch', to='main.branch')),
            ],
        ),
    ]
