from datetime import datetime, timedelta
import datetime
from pytz import timezone
import pytz
import time
from django.utils.timezone import localtime
from django.shortcuts import render
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from decimal import Decimal

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.settings import api_settings

from bid.models import Bid
from bid.serializers import BidSerializer, BidDetailSerializer
from post.models import Post

def get_highest_bid(post_id):
  all_bids = Bid.objects.filter(post=post_id).order_by('-amount')
  post = Post.objects.get(id=post_id)
  time_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
  post_end_time = post.end_time
  
  print('ALL BIDS ', all_bids)
  highest_bid = all_bids[0].amount

  # if the post has ended we will set the sold price 
  if time_now > post_end_time:
    post.sold_price = highest_bid
    post.is_sold = True
    post.save()

  print('HIGHEST BID - ', (highest_bid))
  return highest_bid

# Check if you can bid 
def can_bid(start_time, end_time):
  # time_now = datetime.datetime.now()
  time_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
  print('TIME NOW - ', time_now)
  if end_time >= time_now and start_time < time_now: # https://kodlogs.com/42178/typeerror-cant-compare-offset-naive-and-offset-aware-datetimes OR https://stackoverflow.com/questions/50265555/comparing-two-python-3-datetime-objects-returns-cant-compare-offset-naive-and 
    return True
  return False

# Check if user is owner
def post_owner(post_id):
  post = Post.objects.get(id=post_id)
  print('POST - ', post)
  post_owner = post.user
  print('POST OWNER - ', post_owner)
  return post_owner


# Create Bid view
class BidCreateAPIView(APIView):
  serializer_class = BidSerializer
  permission_classes = (IsAuthenticated, )

  def post(self, request, post_id, *args, **kwargs):

    post = Post.objects.get(id=post_id)
    print('REQUEST USER - ', type(float(request.data["amount"])))
    highest_bid = get_highest_bid(post_id)
    start_time = post.start_time # post["start_time"]
    end_time = post.end_time # post["end_time"]
    five_min_time = timedelta(seconds=300)

    print('---------------')
    print(f"start time - {localtime(start_time)}")
    print(f"end time - {localtime(end_time)}")
    print("CAN BID - ", can_bid(start_time, end_time))
    print('POST ID', post_id)
    print("POST - ", post.no_bids)
    print(five_min_time)
    print('---------------')

    # make sure user making bid is not post owner if user is the same as the user returned from post_owner function
    if request.user.username == post_owner(post_id):
      print('bidder is owner of post')
      return Response({'detail': 'Cannot place a bid if you are owner of the post'}, status=status.HTTP_400_BAD_REQUEST)
    # make sure bid is greater than highest bid
    elif Decimal(request.data["amount"]) <= highest_bid:
      return Response({'detail': 'bid must be greater than current bid'}, status=status.HTTP_400_BAD_REQUEST)
    elif Decimal(request.data["amount"]) == 0.00:
      return Response({'detail': 'bid must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
    # check if you can bid (i.e have enough time)
    elif not can_bid(start_time, end_time):
      return Response({'detail': 'Unable to bid as auction has ended'}, status=status.HTTP_400_BAD_REQUEST)

    # bid = BidSerializer(data=request.data)
    bid_serializer = BidSerializer(data=request.data)
    print(f"start time - {start_time}")
    print("POST ")
    if bid_serializer.is_valid(raise_exception=True):
      bid = Bid(user=request.user, amount=request.data["amount"], post=post)
      bid.save()
      return Response(data=bid_serializer.data, status=201)
    
    # if bid_serializer.is_valid(raise_exception=True):
    #   bid.save(user=request.user)
    #   bid.save(post=post)
    #   return Response(data=bid.data, status=201)

    # sort timezone
    # if timenow is within the last 5 mins of auction
    # when bid is in last 5 mins of auction each new bid adds another 60 seconds
    deadline = post.end_time.strftime("%d/%m/%Y %H:%M:%S")
    d =datetime.datetime.strptime(deadline, "%d/%m/%Y %H:%M:%S")

    if (d - datetime.datetime.now()).total_seconds() < 300:
      post.end_time = post.end_time + datetime.timedelta(seconds=90) # adding 90 seconds
      post.save()
      print("END TIME NOW - ", post.end_time)

# Detail of Bid
@api_view(['GET'])
@permission_classes([AllowAny])
def bid_detail_view(request, bid_id, *args, **kwargs):
  bid_qs = Bid.objects.filter(id=bid_id)
  print('BID ID ---', bid_id)
  if not bid_qs.exists():
    return Response({
      'detail': 'Error Finding Bid'
    }, status=404)
  bid = bid_qs.first()
  serializer = BidDetailSerializer(bid)
  return Response(serializer.data, status=200)

# Get all bids for a post
@api_view(['GET'])
@permission_classes([AllowAny])
def all_bids_view(request, post_id, *args, **kwargs):
  bids_qs = Bid.objects.filter(post_id=post_id)
  print(bids_qs)
  return Response({}, status=200)

# current bid will be the highest bid 






# Get highest bid view
# class HighestBidAPIView(APIView):
#   permission_classes = (AllowAny, )
#   serializer_class = BidSerializer

#   def get_queryset(self, post_id):
#     queryset = Bids.object.filter(post=post_id).order_by('-amount')
#     # queryset = Bids.object.filter(post=post_id).order_by('-amount')[:1].get()
#     print(queryset)
#     highest_bid = queryset[0]
#     return highest_bid