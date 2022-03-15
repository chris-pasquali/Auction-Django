from rest_framework import serializers
from category.models import Category
from post.serializers import PostSerializer

class CategoryListSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Category
    fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Category
    fields = '__all__'
