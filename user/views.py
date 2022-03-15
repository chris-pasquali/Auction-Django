from django.shortcuts import render
import time
from rest_framework.views import APIView
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token 
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)

from user.models import User
from post.models import Post
from user.permissions import UserIsOwner
from post.serializers import PostSerializer, PostListSerializer
from user.serializers import UserSerializer, UserListSerializer, RegistrationSerializer

# Register
# Response: https://gist.github.com/mitchtabian/c13c41fa0f51b304d7638b7bac7cb694
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

  if request.method == 'POST':
    data = {}
    email = request.data.get('email', '0').lower()
    if validate_email(email) != None:
      data['error_message'] = 'That email is already taken'
      data['response'] = 'Error'
      return Response(data)
    
    username = request.data.get('username', '0')
    if validate_username(username) != None:
      data['error_message'] = 'That username is already in use.'
      data['response'] = 'Error'  
      return Response(data)

    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      data['response'] = 'successfully registered new user.'
      data['email'] = user.email
      data['username'] = user.username
      # data['pk'] = user.pk
      token = Token.objects.get(user=user).key
      data['token'] = token
    else:
      data = serializer.errors
    
    return Response(data)

def validate_email(email):
  user = None
  try:
    user = User.objects.get(email=email)
  except User.DoesNotExist:
    return None
  if user != None:
    return email

def validate_username(username):
  user = None
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    return None
  if user != None:
    return username

# LOGIN
# Response: https://gist.github.com/mitchtabian/8e1bde81b3be342853ddfcc45ec0df8a
# URL: http://127.0.0.1:8000/api/account/login
class ObtainAuthTokenView(APIView):
  authentication_classes = []
  permission_classes = []

  def post(self, request):
    context = {}

    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    if user:
      try:
        token = Token.objects.get(user=user)
      except Token.DoesNotExist:
        token = Token.objects.create(user=user)
      context['response'] = 'Successfully authenticated'
      # context['pk'] = user.pk
      context['email'] = email.lower()
      context['token'] = token.key
    else:
      context['response'] = 'Error'
      context['error_message'] = 'Invalid credentials'
    
    return Response(context)
      
@api_view(['GET'])
# @api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):
  if request.method == 'GET': # GET
    email = request.GET['email'].lower()
    # email = request.POST['email'].lower()
    data = {}

    try:
      user = User.objects.get(email=email)
      data['response'] = email
    except User.DoesNotExist:
      data['response'] = 'User does not exist'
    
    return Response(data)

# test register api endpoint
class UserRegistrationAPIView(CreateAPIView):
  serializer_class = UserSerializer

class UserUpdateAPIView(RetrieveUpdateAPIView):
  lookup_url_kwarg = 'username'
  queryset = User.objects.all()
  lookup_field = 'username__iexact'
  serializer_class = UserSerializer
  permission_classes = (IsAuthenticated, UserIsOwner)

class UserDetailAPIView(RetrieveAPIView):
  lookup_url_kwarg = 'username'
  queryset = User.objects.all()
  lookup_field = 'username__iexact'
  serializer_class = UserSerializer # Detail Serializer
  # TODO -> Get number of posts

class UserPostListAPIView(ListAPIView):
  serializer_class = PostListSerializer
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    username = self.kwargs['username']
    user = get_object_or_404(User, username__iexact=username)
    if user.id == self.request.user.id:
      return Post.objects.filter(user__username__iexact=username).order_by('-created_at')
    else:
      raise PermissionDenied('Please log in to see a users post')

# get bids user has created

# get updated status of bids - time remaining on posts and if it is winning bid