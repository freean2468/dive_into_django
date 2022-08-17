from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from typing import List

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .managers import UserManager

# A model is the single, definitive source of information about your data. 
# It contains the essential fields and behaviors of the data you’re storing. 
# Django follows the DRY Principle. The goal is to define your data model 
# in one place and automatically derive things from it.
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField("Email", max_length=64, unique=True)
    nickname = models.CharField("Nickname", max_length=16, unique=True)
    password = models.CharField("Password", max_length=128)
    name = models.CharField("Name", max_length=32)
    phone = models.CharField("Phone", max_length=11, unique=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['nickname', 'password', 'name', 'phone']
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)