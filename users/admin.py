from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from typing import Optional, Sequence

# Register your models here.

from . import models

class UserAdmin(BaseUserAdmin):
    ordering: Optional[Sequence[str]] = ('email', )


# admin.site.unregister(User)
admin.site.register(models.User, UserAdmin)