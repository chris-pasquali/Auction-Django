from django.urls import path

from .views import *

app_name = 'post'

urlpatterns = [
  path('', PostListAPIView.as_view(), name='post-list'),
  path('create/', PostCreateAPIView.as_view(), name='create'),
  # path('create-test/', post_create_view, name='post-test'),
]