from pickle import TRUE
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True


class User(AbstractBaseUser):
    """
    https://docs.djangoproject.com/en/3.2/topics/db/models/
    User class model used for authentication
    """
    usename = models.CharField(max_length=255, unique=TRUE, blank=False)
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    class Meta:
        managed = False
        db_table = "users_user"

    USERNAME_FIELD = "username"

    """
    Any methods on this model will be accessible to all the services.
    """
    def jwt_get_secret_key(self):
        return self.jwt_secret
