from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password, name, phone, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not phone:
            raise ValueError(_('The Phone must be set'))
        if not nickname:
            raise ValueError(_('The Nickname must be set'))
        if not name:
            raise ValueError(_('The Name must be set'))

        email = self.normalize_email(email)

        user = self.model(email=email, phone=phone, nickname=nickname, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nickname, password, name, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, nickname, password, name, phone, **extra_fields)
