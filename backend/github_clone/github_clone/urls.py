"""
URL configuration for github_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from github_clone.settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('auth.urls')),
    path('repository/', include('repository.urls')),
    path('developer/', include('developer.urls')),
    path('branch/', include('branch.urls')),
    path('milestone/', include('milestone.urls')),
    path('pr/', include('pull_request.urls')),
    path('issue/', include('issue.urls')),
    path('commit/', include('commit.urls')),
    path('issue/', include('issue.urls')),
    path('label/', include('label.urls')),
    path('notifications/', include('websocket.urls')),
]

urlpatterns += static("/avatars/", document_root=os.path.join(BASE_DIR, 'avatars'))
