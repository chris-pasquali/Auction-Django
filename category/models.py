from django.db import models

class Category(models.Model):
  class Meta:
    verbose_name = "Category"
    verbose_name_plural = "Categories"
  
  title = models.CharField(max_length=250)
  image = models.ImageField(verbose_name="Category Image", upload_to="category_images/", default="category_images/default.png")

  def __str__(self):
    return self.title
