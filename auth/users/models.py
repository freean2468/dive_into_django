from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import List
from .managers import UserManager


class User(AbstractUser):
    '''
    A model is the single, definitive source of information about your data.
    It contains the essential fields and behaviors of the data you’re storing.
    Django follows the DRY Principle. The goal is to define your data model
    in one place and automatically derive things from it.
    '''
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
