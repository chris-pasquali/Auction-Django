from rest_framework import serializers
from bid.models import Bid
from post.serializers import PostSerializer
from user.serializers import *

class BidSerializer(serializers.ModelSerializer):
  
  user = UserSerializer(source='user.user', read_only=True) # UserSerializer()
  # post = PostSerializer()
  class Meta:
    model = Bid
    # fields = '__all__'
    exclude = ('post',)

class BidDetailSerializer(serializers.ModelSerializer):

  class Meta:
    model = Bid
    fields = '__all__'