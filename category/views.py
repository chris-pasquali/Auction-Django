import time
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

from category.models import Category
from category.serializers import CategoryListSerializer, CategorySerializer
### ###

# TODO - Allow posts to have multiple categories 
# Have other categories other than body types - e.g. sports cars, super cars, off road, luxury cars, muscle cars
# Example - https://www.smartmotorist.com/car-types

# List Categories View
class CategoryListAPIView(ListAPIView):
  serializer_class = CategoryListSerializer
  permission_classes = (AllowAny,)
  queryset = Category.objects.all()

# Add Category View (ADMIN only)
class CategoryCreateAPIView(APIView):
  serializer_class = CategorySerializer
  parser_classes = (MultiPartParser, FormParser, FileUploadParser)
  permission_classes = (IsAuthenticated,) # ADMIN only

  def post(self, request, *args, **kwargs):
    category_serializer = CategorySerializer(data=request.data)
    if category_serializer.is_valid(raise_exception=True):
      category_serializer.save()
      return Response(category_serializer.data, status=201)
    return Response({}, status=400)


# Delete Category View (Admin only)
# class DeleteCategoryAPIView(APIView):
#   serializer_class = CategorySerializer
#   permission_classes = (IsAuthenticated, ) # ADMIN only

#   def delete(self, request, pk):
#     category_to_delete = Category.objects.filter(id=pk)
#     if not category_to_delete.exists():
#       return Response({}, status=404)

# ADMIN ONLY
@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def category_delete_view(request, category_id, *args, **kwargs):
    category_to_delete = Category.objects.filter(id=category_id)
    if not category_to_delete.exists():
        return Response({"message": "Category does not exist"}, status=404)
    # Make sure the user is an ADMIN
    # qs = qs.filter(user=request.user)
    # if not qs.exists():
    #     return Response({"message": "You cannot delete this category"}, status=401)
    category_to_delete.delete()
    return Response({"message": "Category removed"}, status=200)
    



