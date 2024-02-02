from django.urls import path
from developer.views import *

urlpatterns = [
    path('update/<str:username>/', UpdateUserView.as_view(), name='update_developer_username'),
    path('<str:username>/', get_users_info, name='get_user_info'),
    path('gitea/<str:username>/', get_gitea_user_info, name='get_gitea_user_info'),
    path('avatar/<str:username>/', get_developer_avatar, name='get_developer_avatar'),
]