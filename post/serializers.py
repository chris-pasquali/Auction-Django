from rest_framework import serializers

from .models import Post, Image
from user.serializers import *

class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = '__all__'
    # fields = ['file']

class ImageListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ['file']

class PostSerializer(serializers.ModelSerializer):

  # user = userListSerializer()
  # bids = bidsSerialier()
  # images = ImageListSerializer()
  user = UserSerializer(source='user.user', read_only=True) # UserSerializer()
  # images = ImageSerializer(many=True, required=False)

  class Meta:
    model = Post
    fields = '__all__'
  
  # def get_bids(self, obj):
  #   return obj.bids.count()

class PostDetailSerializer(serializers.ModelSerializer):
   # user = userListSerializer()
  # bids = bidsSerialier()
  # images = ImageListSerializer()
  user = UserSerializer(source='user.user', read_only=True) # UserSerializer()
  images = ImageSerializer(many=True, required=False)

  class Meta:
    model = Post
    fields = '__all__'
  
  # def get_bids(self, obj):
  #   return obj.bids.count()

class PostListSerializer(serializers.ModelSerializer):
  user = UserListSerializer()
  images = ImageListSerializer(many=True)

  class Meta:
    model = Post
    fields = '__all__'

class PostCreateSerializer(serializers.ModelSerializer):
  user = UserSerializer(source='user.user', read_only=True) # UserSerializer()
  images = ImageSerializer(many=True, required=False)
  #images = ImageListSerializer(many=True)

  class Meta:
    model = Post
    fields = '__all__'
  
  def create(self, validated_data):
    """
    Handle writable nested serializer to create a new post.
    :param validated_data: validated data, by serializer class's validate method
    :return: updated Post model instance
    """
    # TODO: Handle the case to avoid new Post instance creation if Image model data have any errors
    data = validated_data.copy()
    data.pop('images') # deleting 'images' list as it is not going to be used

    '''
    Fetching `images` list of image files explicitly from context.
    Because using default way, value of `images` received at serializers from viewset was an empty list.
    However value of `images` in viewset were OK.
    Hence applied this workaround.
    '''
    images_data = self.context.get('request').data.pop('images')
    try:
      post = Post.objects.create(**data)
    except TypeError:
      msg = (
        'Got a `TypeError` when calling `Post.objects.create()`.'
      )
      raise TypeError(msg)
    try:
      for image_data in images_data:
        # Image.objects.create(post=post, **image_data)
        image, created = Image.objects.get_or_create(image=image_data)
        post.images.add(image)
      return post
    except TypeError:
      post = Post.objects.get(pk=post.id)
      post.delete()
      msg = (
        'Got a `TypeError` when calling `Image.objects.get_or_create()`.'
      )
      raise TypeError(msg)

    return post
  

  def update(self, instance, validated_data):
    """
    Handle writable nested serializer to update the current post.
    :param instance: current Post model instance
    :param validated_data: validated data, by serializer class's validate method
    :return: updated Post model instance
    """
    # TODO: change the definition to make it work same as create()

    '''
    overwrite post instance fields with new data if not None, else assign the old value
    '''
    instance.user = validated_data.get('user', instance.user)
    instance.category = validated_data.get('category', instance.category)
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.featured = validated_data.get('featured', instance.featured)
    instance.is_sold = validated_data.get('is_sold', instance.is_sold)
    instance.starting_price = validated_data.get('starting_price', instance.starting_price)
    instance.min_increase = validated_data.get('min_increase', instance.min_increase)
    instance.start_time = validated_data.get('start_time', instance.start_time)
    instance.end_time = validated_data.get('end_time', instance.end_time)
    instance.sold_price = validated_data.get('sold_price', instance.sold_price)

    instance.town = validated_data.get('town', instance.town)
    instance.state = validated_data.get('state', instance.state)
    instance.postcode = validated_data.get('postcode', instance.postcode)
    instance.condition = validated_data.get('condition', instance.condition)
    instance.seller_type = validated_data.get('seller_type', instance.seller_type)

    instance.make = validated_data.get('make', instance.make)
    instance.model = validated_data.get('model', instance.model)
    instance.variant = validated_data.get('variant', instance.variant)
    instance.badge = validated_data.get('badge', instance.badge)
    instance.odometer = validated_data.get('odometer', instance.odometer)
    instance.year = validated_data.get('year', instance.year)
    instance.model_year = validated_data.get('model_year', instance.model_year)
    instance.engine = validated_data.get('engine', instance.engine)
    instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)
    instance.drive_type = validated_data.get('drive_type', instance.drive_type)
    instance.exterior_color = validated_data.get('exterior_color', instance.exterior_color)
    instance.interior_color = validated_data.get('interior_color', instance.interior_color)
    instance.transmission = validated_data.get('transmission', instance.transmission)
    instance.body_type = validated_data.get('body_type', instance.body_type)
    instance.seats = validated_data.get('seats', instance.seats)
    instance.reg_exp = validated_data.get('reg_exp', instance.reg_exp)
    instance.vin = validated_data.get('vin', instance.vin)

    try:
      '''
      Fetching `images` list of image files explicitly from context.
      Because using default way, value of `images` received at serializers from viewset was an empty list.
      However value of `images` in viewset were OK.
      Hence applied this workaround.   
      '''
      images_data = self.context.get('request').data.pop('images')
    except:
      images_data = None
    
    if images_data is not None:
      image_instance_list = []
      for image_data in images_data:
        image, created = Image.objects.get_or_create(image=image_data)
        image_instance_list.append(image)

      instance.images.set(image_instance_list)
    instance.save()  # why? see base class code; need to save() to make auto_now work
    return instance

  def get_bids(self, obj):
    return obj.bids.count()

