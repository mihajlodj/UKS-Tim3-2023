from django.conf.urls.static import static
from django.urls import path
from developer.views import *
from github_clone.settings import BASE_DIR

urlpatterns = [
    path('update/<str:username>/', UpdateUserView.as_view(), name='update_developer_username'),
    path('update/password/<str:username>/', change_users_password, name='change_users_password'),
    path('newEmail/<str:username>/', add_new_email, name='add_new_email'),
    path('delete/self/<str:username>/<str:usersPassowrd>', delete_user_developer, name='delete_user_developer'),
    path('delete/email/<str:username>/<str:usersEmail>', delete_developers_email, name='delete_developers_email'),
    path('delete/avatar/<str:username>', delete_developers_avatar, name='delete_developers_avatar'),
    path('updateAvatar/<str:username>/', update_developers_avatar, name='update_developer_avatar'),
    path('<str:username>/', get_users_info, name='get_user_info'),
    path('gitea/<str:username>/', get_gitea_user_info, name='get_gitea_user_info'),
    path('avatar/<str:username>/', get_developer_avatar, name='get_developer_avatar'),
    # path('emails/gitea/<str:username>/', get_developers_emails_gitea, name='get_developer_emails'),
    path('emails/<str:username>/', get_developers_emails, name='get_developer_emails'),
    path('all', get_developers, name='get_developers'),
]
urlpatterns += static("/avatars/", document_root=os.path.join(BASE_DIR, 'avatars'))