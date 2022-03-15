from django.db import models

from post.models import Post

class Bid(models.Model):

  # STATUS_ = (
  #   ('W', 'Wining'),
  #   ('L', 'Losing'),
  # )

  user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='bids')
  amount = models.DecimalField(decimal_places=2, max_digits=10)
  date_made = models.DateField(auto_now_add=True)
  # post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_bids")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_bids")

  # status = models.CharField(max_length=1, choices=STATUS_)

  def __str__(self):
    # return str(self.amount)
    return '{} - {}'.format(str(self.amount), self.id)
    # return 'Bid - {} {}',format(self.user.username, str(self.amount))
