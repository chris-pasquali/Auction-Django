from django.urls import path, include

urlpatterns = [
  path('post/', include('post.urls')),
  path('user/', include('user.urls')),
  path('bid/', include('bid.urls')),
]