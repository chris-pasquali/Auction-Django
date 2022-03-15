from django.urls import path

from bid.views import *

app_name = 'bid'

urlpatterns = [
  path('create/<post_id>/', BidCreateAPIView.as_view(), name='create-bid'),
  path('<post_id>/highest_bid/', get_highest_bid, name='highest-bid'),
  path('detail/<bid_id>/', bid_detail_view, name='bid-detail'),
  path('all-bids/<post_id>/', all_bids_view, name="all-bids"),
  # path('', PostListAPIView.as_view(), name='post-list'),
  # path('create/', PostCreateAPIView.as_view(), name='create'),
  # path('create-test/', post_create_view, name='post-test'),
]