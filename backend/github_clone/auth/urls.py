from django.urls import path
from auth.views import RegisterView, confirm_registration, MyObtainTokenPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('register-confirm/', confirm_registration, name='auth_register_confirm'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
]
