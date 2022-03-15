from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, AbstractBaseUser,
    UserManager as AbstractUserManager,
)
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(AbstractUserManager):
  def get_by_natural_key(self, username):
    case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
    return self.get(**{case_insensitive_username_field: username})

  # https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model - https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
  # https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model

class User(AbstractUser):
  username = models.CharField(_('username'), max_length=250, unique=True)
  email = models.EmailField(_('email address'), unique=True)
  first_name = models.CharField(_('first name'), max_length=50)
  last_name = models.CharField(_('last name'), max_length=50)
  profile_picture = models.ImageField(
    null=True,
    blank=True,
    default='default.png',
    upload_to='profile_pictures',
    verbose_name=_('profile picture'),
  )
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)  # a admin user; non super-user
  is_admin = models.BooleanField(default=False)

  # REQUIRED_FIELDS = ['email', 'password']
  REQUIRED_FIELDS = []

  objects = UserManager()

  def __str__(self):
    return self.email

  def get_full_name(self):
    return self.first_name + ' ' + self.last_name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)