from django.http import Http404
import pytest
from django.contrib.auth.models import User
from requests import Response
from main.models import Developer, Project, WorksOn, Branch, PullRequest, PullRequestStatus, Milestone
from faker import Faker
from django.utils import timezone
from pull_request import service, diff_parser

fake = Faker()
email = 'fake.email@gmail.com'
username1 = 'MyUsername'
username2 = 'MyUsername2'
password = 'MyPassword123'
repo_name = 'MyNewTestRepo'
repo_name2 = 'MyNewTestRepo2'
pull_title = 'Title'


@pytest.fixture
def create_developers():
    user1 = User.objects.create_user(username=username1, password=password)
    dev1 = Developer.objects.create(user=user1)
    user2 = User.objects.create_user(username=username2, password=password)
    dev2 = Developer.objects.create(user=user2)
    return dev1, dev2

@pytest.fixture(autouse=True)
def save_repository(create_developers):
    dev1, dev2 = create_developers
    repo = Project.objects.create(name=repo_name, description=fake.text, access_modifier='Private')
    main = Branch.objects.create(name='main', project=repo, created_by=dev1)
    develop = Branch.objects.create(name='develop', project=repo, parent=main, created_by=dev2)
    branch1 = Branch.objects.create(name='branch1', project=repo, parent=develop, created_by=dev2)
    branch2 = Branch.objects.create(name='branch2', project=repo, parent=branch1, created_by=dev1)
    branch3 = Branch.objects.create(name='branch3', project=repo, parent=branch1, created_by=dev1)
    repo.default_branch = main
    repo.save()
    WorksOn.objects.create(role='Owner', project=repo, developer=dev1)
    WorksOn.objects.create(role='Maintainer', project=repo, developer=dev2)
    return repo, main, develop, branch1, branch2, branch3

@pytest.fixture(autouse=True)
def save_pull_requests(create_developers, save_repository):
    dev1, dev2 = create_developers
    repo, main, develop, branch1, branch2, branch3 = save_repository
    milestone = Milestone.objects.create(title='Milestone', deadline=timezone.localtime(timezone.now()), project=Project.objects.get(name=repo_name))
    PullRequest.objects.create(title=pull_title, source=branch3, target=develop, project=repo, author=dev1, status=PullRequestStatus.OPEN, mergeable=True, gitea_id=10)
    PullRequest.objects.create(source=branch1, target=develop, project=repo, author=dev2, status=PullRequestStatus.CLOSED, gitea_id=11)
    PullRequest.objects.create(source=branch2, target=branch1, project=repo, author=dev1, assignee=dev1, status=PullRequestStatus.MERGED, gitea_id=12)
    PullRequest.objects.create(source=branch3, target=branch1, project=repo, author=dev1, status=PullRequestStatus.OPEN, mergeable=False, gitea_id=13, milestone=milestone)

@pytest.fixture()
def save_milestone():
    milestone = Milestone.objects.create(title='Milestone1', deadline=timezone.localtime(timezone.now()), project=Project.objects.get(name=repo_name))
    return milestone

@pytest.mark.django_db
def test_save_pull_request_with_milestone_and_assignee_success(save_milestone):
    milestone = save_milestone
    data = {
        'base': 'main',
        'compare': 'develop',
        'title': 'Title',
        'description': 'Description',
        'assignee': username2,
        'milestone_id': milestone.id
    }
    response = Response()
    content = {'number': 1, 'mergeable': True}
    response.json = lambda: content
    response.status_code = 201
    id = service.save_pull_request(username1, username1, repo_name, data, response)
    assert id == 1
    assert PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).status == PullRequestStatus.OPEN
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).assignee.user.username == username2
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).milestone.id == milestone.id

@pytest.mark.django_db
def test_save_pull_request_with_milestone(save_milestone):
    milestone = save_milestone
    data = {
        'base': 'main',
        'compare': 'develop',
        'title': 'Title',
        'description': 'Description',
        'milestone_id': milestone.id
    }
    response = Response()
    content = {'number': 1, 'mergeable': True}
    response.json = lambda: content
    response.status_code = 201
    id = service.save_pull_request(username1, username1, repo_name, data, response)
    assert id == 1
    assert PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).status == PullRequestStatus.OPEN
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).assignee is None
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).milestone.id == milestone.id

@pytest.mark.django_db
def test_save_pull_request_assignee_success():
    data = {
        'base': 'main',
        'compare': 'develop',
        'title': 'Title',
        'description': 'Description',
        'assignee': username2
    }
    response = Response()
    content = {'number': 1, 'mergeable': True}
    response.json = lambda: content
    response.status_code = 201
    id = service.save_pull_request(username1, username1, repo_name, data, response)
    assert id == 1
    assert PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).status == PullRequestStatus.OPEN
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).assignee.user.username == username2
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).milestone is None

@pytest.mark.django_db
def test_save_pull_request_no_milestone_or_assignee_success():
    data = {
        'base': 'main',
        'compare': 'develop',
        'title': 'Title',
        'description': 'Description'
    }
    response = Response()
    content = {'number': 1, 'mergeable': True}
    response.json = lambda: content
    response.status_code = 201
    id = service.save_pull_request(username1, username1, repo_name, data, response)
    assert id == 1
    assert PullRequest.objects.filter(gitea_id=1, project__name=repo_name).exists()
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).status == PullRequestStatus.OPEN
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).assignee is None
    assert PullRequest.objects.get(gitea_id=1, project__name=repo_name).milestone is None

@pytest.mark.django_db
def test_save_update_milestone_success(save_milestone):
    milestone = save_milestone
    data = { 'milestone_id': milestone.id }
    req = PullRequest.objects.get(gitea_id=10)
    assert req.milestone is None
    service.update_milestone(data, req)
    assert req.milestone.id == milestone.id

@pytest.mark.django_db
def test_save_update_milestone_none_success():
    req = PullRequest.objects.get(gitea_id=13)
    assert req.milestone is not None
    service.update_milestone({}, req)
    assert req.milestone is None

@pytest.mark.django_db
def test_save_update_milestone_throws_404():
    data = { 'milestone_id': 1600 }
    req = PullRequest.objects.get(gitea_id=13)
    assert req.milestone is not None
    with pytest.raises(Http404):
        service.update_milestone(data, req)
    assert req.milestone is not None
    assert req.milestone.id != 1600

@pytest.mark.django_db
def test_save_update_assignee_success():
    data = { 'assignee_username': username2 }
    req = PullRequest.objects.get(gitea_id=11)
    assert req.assignee is None
    service.update_assignee(data, req, username1, repo_name)
    assert req.assignee is not None
    assert req.assignee.user.username == username2

@pytest.mark.django_db
def test_save_update_assignee_none_success():
    req = PullRequest.objects.get(gitea_id=12)
    assert req.assignee is not None
    service.update_assignee({}, req, username1, repo_name)
    assert req.assignee is None

@pytest.mark.django_db
def test_save_update_assignee_throws_404():
    data = { 'assignee_username': 'does not exist' }
    req = PullRequest.objects.get(gitea_id=12)
    assert req.assignee is not None
    assert req.assignee.user.username == username1
    with pytest.raises(Http404):
        service.update_assignee(data, req, username1, repo_name)
    assert req.assignee is not None
    assert req.assignee.user.username == username1

@pytest.mark.django_db
def test_get_pr_from_merge_commit_success():
    msg = "Merge pull request 'Another pull' (#12) from abcdef into develop"
    pull = service.get_pull_request_from_merge_commit(msg, repo_name)
    assert pull is not None
    assert pull.gitea_id == 12


@pytest.mark.django_db
def test_diff_parse_success():
    string = '''diff --git a/test.pdf b/test.pdf
deleted file mode 100644
index e05dcaf..0000000
Binary files a/test.pdf and /dev/null differ
diff --git a/abc.txt b/abc.txt
new file mode 100644
index 0000000..439fa1d
--- /dev/null
+++ b/abc.txt
@@ -0,0 +1,8 @@
+fdsgadsfbgadfbad
+
+ovo je 1
+some content
+neki novi
+sadrzaj
+dfklvmldfnb
+dcbmkaldmvb
diff --git a/myfile.txt b/myfile.txt
index 11ac595..c043e6b 100644
--- a/myfile.txt
+++ b/myfile.txt
@@ -1 +1,3 @@
-vdfbdfbadb dfvXv
+vdfbdfbb dfvXv
+editing
+content
'''
    diff, overall_additions, overall_deletions = diff_parser.parse_diff(string)
    assert overall_additions == 11
    assert overall_deletions == 1
    assert len(diff) == 3
    assert diff[0]['mode'] == 'delete'
    assert diff[0]['file_path'] == 'test.pdf'
    assert len(diff[0]['content']) == 0
    assert diff[0]['additions'] == 0
    assert diff[0]['deletions'] == 0

    assert diff[1]['mode'] == 'add'
    assert diff[1]['file_path'] == 'abc.txt'
    assert len(diff[1]['content']) == 8
    assert diff[1]['additions'] == 8
    assert diff[1]['deletions'] == 0

    assert diff[2]['mode'] == 'update'
    assert diff[2]['file_path'] == 'myfile.txt'
    assert len(diff[2]['content']) == 4
    assert diff[2]['additions'] == 3
    assert diff[2]['deletions'] == 1
