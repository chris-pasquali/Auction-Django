import time
import datetime
from django.db.models import QuerySet
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.settings import api_settings

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostDetailSerializer, ImageSerializer


class PostListAPIView(ListAPIView):
  serializer_class = PostSerializer
  permission_classes = (AllowAny,)
  queryset = Post.objects.all()
  # Sort by newest

# Get Posts by category view
class PostsByCategoryAPIView(ListAPIView):
  serializer_class = PostSerializer
  permission_classes = (AllowAny,)
  
  def get_queryset(self):
    return Post.objects.filter(category=self.kwargs['category'])

# Post Create View 
class PostCreateAPIView(APIView):
  permission_classes = (IsAuthenticated,)
  # permission_classes = (AllowAny,)
  parser_classes = (MultiPartParser, FormParser, FileUploadParser)
  serializer_class = PostSerializer

  def post(self, request, *args, **kwargs):
    resp = {'error': ''}

    print(request.user.username)
    print('-----------')
    # print(request.FILES.getlist('images'))
    # print(request.POST.get('id'))
    print(request.data)
    post = PostSerializer(data=request.data)
    images = request.FILES.getlist('images')
    # print(images)
    if post.is_valid(raise_exception=True):
      post.save(user=request.user)
      print(post.data['id'])
      for image in images:
        image_data = {
          'file': image,
          'post': post.data['id']
        }
        
        image_serializer = ImageSerializer(data=image_data)
        if image_serializer.is_valid():
          image_serializer.save()
        else:
          resp['error'] = 'Invalid image data'
          break
      
      return Response(post.data, status=201)
    # if no photos upload default

    return Response({}, status=400)

# Post Update View
class PostUpdateAPIView(APIView):
  permission_classes = (IsAuthenticated,)
  # permission_classes = (AllowAny,)
  parser_classes = (MultiPartParser, FormParser, FileUploadParser)

  def get(self, request, pk):
    try:
      # Check whether user owns post 
      post = Post.objects.filter(request.user).get(pk=pk)
    except Post.DoesNotExist:
      return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
      return Response(PostSerializer(post).data)
  
  def put(self, request, pk):
    try:
      post = Post.objects.filter(user=request.user).get(pk=pk)
    except Post.DoesNotExist:
      return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    #provide a list of images that you want to delete
    images_to_delete = set(map(int, request.POST.getlist('to_delete')))

    # list of images you want to add
    additional_images = request.FILES.getlist('images')

    post_images = post.images.all()
    post_images_count = post_images.count()

    final_images_count = post_images_count - len(images_to_delete) + len(additional_images)

    # If the datetime.now is passed end date then post cannot be updated
    time_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

    if time_now > post.end_time:
      return Response({
        'detail': 'Cannot update a post that has already ended'
      }, status=status.HTTP_400_BAD_REQUEST)

    if final_images_count > 10 or final_images_count <= 0:
      return Response(
        {'detail': 'Cannot have more than 10 images or a post with 0 images'},
        status=status.HTTP_400_BAD_REQUEST
      )
    elif images_to_delete.issubset(set(post_images.values_list('pk', flat=True))):
      # Default case if everything goes right since only two situations can evaluate
      # the above clause to be true -
      #   1. Either no new images were provided and thus an empty set will always be
      #      a subset to all the images already existing in the post OR
      #   2. The ids that were provided in to_delete were valid ids that belong to the
      #      id list of the images reversely to the post.
      post_images.filter(id__in=images_to_delete).delete()

      for image in additional_images:
        image_data = {
          'file': image,
          'post': post.data['id']
        }
        image_serializer = ImageSerializer(data=image_data)
        if image_serializer.is_valid():
          image_serializer.save()
        else:
          return Response(
            {'error': 'Invalid image data'},
            status=status.HTTP_409_CONFLICT,
          )

# Post Delete View TODO

# Post Detail View
@api_view(['GET'])
@permission_classes([AllowAny])
def post_detail_view(request, post_id, *args, **kwargs):
  qs = Post.objects.filter(id=post_id)
  if not qs.exists():
    return Response({}, status=404)
  obj = qs.first()
  serializer = PostSerializer(obj) # PostDetailSerializer
  return Response(serializer.data, status=200)

class PostDetailAPIView(APIView):
  # permission_classes = (IsAuthenticated,)
  permission_classes = (AllowAny,)
  parser_classes = (MultiPartParser, FormParser, FileUploadParser)

  def get_object(self, post_id, user_id):
    '''
    Helper method to get the object with given post_id and user_id
    '''
    try:
      return Post.objects.get(id=post_id, user=user_id)
    except Post.DoesNotExist:
      return None
  
  def get(self, request, post_id, *args, **kwargs):
    '''
    Retreives the Post with given post_id
    '''
    post = self.get_object(post_id, request.user.id)
    if not post:
      return Response(
        {"res": "Object with post id does not exists"},
        status=400
      )
    post_serializer = PostDetailSerializer(post)
    return Response(post_serializer.data, status=200)
  
  def put(self, request, post_id, *args, **kwargs):
    '''
    Updates the post item if the post_id exists
    '''
    post = self.get_object(post_id, request.user.id)
    if not post:
      return Response(
        {"res": "Object with post id does not exists"}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    post_serializer = PostSerializer(data=request.data)
    images = request.FILES.getlist('images')
    # print(images)
    if post_serializer.is_valid():
      post_serializer.save()
      print(post.data['id'])
      for image in images:
        image_data = {
          'file': image,
          'post': post_id # post.data['id']
        }
        
        image_serializer = ImageSerializer(data=image_data)
        if image_serializer.is_valid():
          image_serializer.save()
        else:
          return Response(
            {"res": "Invalid image data"}, 
            status=status.HTTP_400_BAD_REQUEST
          )
          # break
      return Response(post_serializer.data, status=200)

# Most Popular Posts View - TODO

# Get Featured Posts
class FeaturedPostListAPIView(ListAPIView):

  serializer_class = PostSerializer

  def get_queryset(self):
    feaured_posts = Post.objects.filter(featured=True)
    return feaured_posts

# Posts almost ending view - next 24 hours TODO

# Sold Posts View
class SoldPostsListAPIView(ListAPIView):

  serializer_class = PostSerializer

  def get_queryset(self):
    '''
    This will return a list of posts where is_sold = True
    '''
    sold_posts = Post.objects.filter(is_sold=True)
    return sold_posts

# Get live items and get posts coming soon TODO

# SEARCH FUNCTIONALITY TODO

# What happens when time ends - winning bid

# If user has winning bid

# sort by category

