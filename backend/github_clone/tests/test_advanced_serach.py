import pytest
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User
from developer.views import get_all_commits, get_all_devs
from repository.views import get_all_repos
from issue.views import get_all_issues
from pull_request.views import get_all_pull_reqs
from main.models import Developer, Project, Issue, PullRequest, Commit, WorksOn, Role, Branch


@pytest.fixture
def setup_data():
    user1 = User.objects.create_user(username="john_doe", password="password")
    user2 = User.objects.create_user(username="jane_smith", password="password")

    dev1 = Developer.objects.create(user=user1)
    dev2 = Developer.objects.create(user=user2)

    project1 = Project.objects.create(name="sample_project_1")
    project2 = Project.objects.create(name="sample_project_2")

    branch1 = Branch.objects.create(name="sample_branch_1", project=project1)
    branch2 = Branch.objects.create(name="sample_branch_2", project=project2)

    WorksOn.objects.create(developer=dev1, project=project1, role=Role.OWNER)
    WorksOn.objects.create(developer=dev1, project=project2, role=Role.OWNER)
    WorksOn.objects.create(developer=dev2, project=project2, role=Role.DEVELOPER)

    issue1 = Issue.objects.create(title="sample_issue_1", project=project1, creator=dev1)
    issue2 = Issue.objects.create(title="sample_issue_2", project=project2, creator=dev2)

    pr1 = PullRequest.objects.create(title="sample_pr_1", project=project1, author=dev1, source=branch1,
                                     target=branch1)
    pr2 = PullRequest.objects.create(title="sample_pr_2", project=project2, author=dev2, source=branch2,
                                     target=branch2)

    commit1 = Commit.objects.create(message="sample_commit_1", author=dev1, branch=branch1, committer=dev1)
    commit2 = Commit.objects.create(message="sample_commit_2", author=dev2, branch=branch2, committer=dev2)


@pytest.mark.django_db
def test_get_all_issues(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/issue/')
    response = get_all_issues(request, query="iss&is:open")
    assert response.status_code == status.HTTP_200_OK
    assert response.data
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_all_pull_reqs(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/pr/')
    response = get_all_pull_reqs(request, query="pr&is:open")
    assert response.status_code == status.HTTP_200_OK
    assert response.data
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_all_commits(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/developer/')
    response = get_all_commits(request, query="com")
    assert response.status_code == status.HTTP_200_OK
    assert response.data
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_all_devs(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/developer/')
    response = get_all_devs(request, query="j")
    assert response.status_code == status.HTTP_200_OK
    assert response.data
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_all_repos(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/repository/')
    response = get_all_repos(request, query="pro")
    assert response.status_code == status.HTTP_200_OK
    assert response.data
    assert len(response.data) == 2


@pytest.mark.django_db
def test_invalid_query_get_all_issues(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/issue/')
    response = get_all_issues(request, query="invalid_query_string")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_no_results_get_all_pull_reqs(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/pr/')
    response = get_all_pull_reqs(request, query="pr&is:closed")
    assert response.status_code == status.HTTP_200_OK
    assert not response.data


@pytest.mark.django_db
def test_get_all_commits_no_results(setup_data):
    factory = APIRequestFactory()
    request = factory.get('/api/developer/')
    response = get_all_commits(request, query="com&author:john")
    assert response.status_code == status.HTTP_200_OK
    assert not response.data
