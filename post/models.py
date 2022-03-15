from django.db import models
from datetime import datetime
from typing import List
from django.core.exceptions import SuspiciousOperation
# from taggit.managers import TaggableManager

from category.models import Category

class Post(models.Model):
  user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='posts')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
  title = models.CharField(max_length=250, verbose_name="Post title")
  description = models.TextField(verbose_name="Post description")
  featured = models.BooleanField(default=False)
  is_sold = models.BooleanField(default=False)
  starting_price = models.DecimalField(decimal_places=2, max_digits=10) # or make a reserve
  min_increase = models.DecimalField(decimal_places=2, max_digits=10)
  start_time = models.DateTimeField(null=True, blank=True)
  end_time = models.DateTimeField(null=True, blank=True)
  sold_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

  town = models.CharField(max_length=250)
  state = models.CharField(max_length=250)
  postcode = models.CharField(max_length=5)
  
  condition = models.CharField(max_length=150, verbose_name="Car Condition") # Choice Field
  seller_type = models.CharField(max_length=150, verbose_name="Seller Type") # Choice Field

  make = models.CharField(max_length=150, verbose_name="Car Make")
  model = models.CharField(max_length=150, verbose_name="Car Model")
  variant = models.CharField(max_length=150, null=True, blank=True, verbose_name="Car Variant")
  badge = models.CharField(max_length=150, verbose_name="Car Badge")
  odometer = models.IntegerField(verbose_name="Car Odometer")
  year = models.CharField(max_length=4, verbose_name="Car Year")
  model_year = models.CharField(max_length=4, null=True, blank=True, verbose_name="Car Model Year")
  engine = models.CharField(max_length=50, verbose_name="Car Engine")
  fuel_type = models.CharField(max_length=50, verbose_name="Car Fuel Type")
  drive_type =models.CharField(max_length=50, verbose_name="Car Drive Type")
  exterior_color = models.CharField(max_length=50, verbose_name="Car Exterior Color")
  interior_color = models.CharField(max_length=50, verbose_name="Car Interior color")
  transmission = models.CharField(max_length=150, verbose_name="Car Transmission") # Choice Field
  body_type = models.CharField(max_length=150, verbose_name="Car Body Type") # Choice Field
  seats = models.CharField(max_length=10, verbose_name="Car Seats")
  reg_exp = models.DateField(null=True, blank=True)
  vin = models.CharField( verbose_name="Car VIN", max_length=250, null=True, blank=True)

  created_at = models.DateField(auto_now_add=True)
  # tags = TaggableManager()

  # have a model function that gets the sold price when auction is finished

  @property
  def image_links(self): # def image_links(self) -> models.QuerySet:
    return self.images.values_list('file', flat=True)
  
  # @property
  def no_bids(self):
    return self.post_bids.count()

  class Meta:
    indexes: List[models.Index] = [
      models.Index(fields=('user',)),
    ]
  
  def __str__(self):
    return self.user.username
    # return self.title

class Image(models.Model):
  file = models.ImageField(upload_to='post_images/')
  post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='images')

  class Meta:
    indexes: List[models.Index] = [
      models.Index(fields=('post',)),
    ]
  
  def save(self, *args, **kwargs):
    """ Sanitary check for a post having more than or equal to 10 images. """
    if self.post.images.count() >= 10:
      raise SuspiciousOperation('Post already contains 5 images.')
    else:
      super().save(*args, **kwargs)

  def __str__(self):
    # return self.post
    return '{} by {}'.format(self.file, self.post.id)
  
