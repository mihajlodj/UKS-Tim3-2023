from django.urls import path
from developer.views import *

urlpatterns = [
    path('update/<str:username>/', UpdateUserView.as_view(), name='update_developer_username'),
    path('update/password/<str:username>/', change_users_password, name='change_users_password'),
    path('updateAvatar/<str:username>/', update_developers_avatar, name='update_developer_avatar'),
    path('<str:username>/', get_users_info, name='get_user_info'),
    path('gitea/<str:username>/', get_gitea_user_info, name='get_gitea_user_info'),
    path('avatar/<str:username>/', get_developer_avatar, name='get_developer_avatar'),
    path('emails/<str:username>/', get_developers_emails, name='get_developer_emails'),
]