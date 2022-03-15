from django.urls import path
from user.views import (
  registration_view,
  ObtainAuthTokenView,
  does_account_exist_view,
  UserRegistrationAPIView,
  UserUpdateAPIView,
  UserDetailAPIView,
  UserPostListAPIView,
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
  path('check_if_account_exists/', does_account_exist_view, name='check_if_account_exists'),
  path('login', obtain_auth_token, name='login-test'), # send a request containing username and password
  
  path('register', registration_view, name='register'),
  path('update/<slug:username>/', UserUpdateAPIView.as_view(), name='update'),
  path('posts/<slug:username>/', UserPostListAPIView.as_view(), name='posts'),
  path('details/<slug:username>/', UserDetailAPIView.as_view(), name='detail'),

  # Test endpoints
  path('register-test', UserRegistrationAPIView.as_view(), name='register-test'),
  path('login-test', ObtainAuthTokenView.as_view(), name='login'),
]