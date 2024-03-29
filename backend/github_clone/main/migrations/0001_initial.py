# Generated by Django 4.2.7 on 2024-02-12 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gitea_token', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.CharField(blank=True, max_length=1000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('caused_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caused_events', to='main.developer')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='managed_issues', to='main.developer')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('access_modifier', models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], default='Public', max_length=10)),
                ('default_branch', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_branch', to='main.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.event')),
                ('content', models.TextField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.comment')),
            ],
            bases=('main.event',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.event')),
                ('name', models.CharField(max_length=255)),
            ],
            bases=('main.event',),
        ),
        migrations.CreateModel(
            name='WorksOn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Unregistered', 'Unregistered'), ('Readonly', 'Readonly'), ('Developer', 'Developer'), ('Maintainer', 'Maintainer'), ('Owner', 'Owner'), ('IsBanned', 'IsBanned')], default='Developer', max_length=20)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.developer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='Watches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.developer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='main.developer')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contains', to='main.issue')),
            ],
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.developer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='SecondaryEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('primary', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.developer')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Merged', 'Merged')], default='Open', max_length=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pull_requests_author', to='main.developer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
                ('reviewers', models.ManyToManyField(related_name='pull_requests_reviewers', to='main.developer')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pull_requests_source', to='main.branch')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pull_requests_target', to='main.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateField()),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('state', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=10)),
                ('id_from_gitea', models.IntegerField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestones', to='main.project')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='main.milestone'),
        ),
        migrations.CreateModel(
            name='Fork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.developer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='issue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_events', to='main.issue'),
        ),
        migrations.AddField(
            model_name='event',
            name='milestone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='milestone_events', to='main.milestone'),
        ),
        migrations.AddField(
            model_name='event',
            name='pull_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pull_request_events', to='main.pullrequest'),
        ),
        migrations.AddField(
            model_name='branch',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='main.developer'),
        ),
        migrations.AddField(
            model_name='branch',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branches', to='main.branch'),
        ),
        migrations.AddField(
            model_name='branch',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='main.project'),
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='main.developer')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='main.comment')),
            ],
        ),
        migrations.CreateModel(
            name='ContentChanged',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.event')),
                ('new_content', models.TextField()),
                ('changer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changer', to='main.developer')),
            ],
            bases=('main.event',),
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField(blank=True, null=True)),
                ('additional_description', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_commits', to='main.developer')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to', to='main.branch')),
                ('committer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committed_commits', to='main.developer')),
                ('tags', models.ManyToManyField(blank=True, related_name='commits', to='main.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.event')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assignments', to='main.developer')),
            ],
            bases=('main.event',),
        ),
    ]
