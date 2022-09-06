from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from typing import Optional, Sequence
from django.utils.translation import gettext_lazy as _
from . import models


class UserAdmin(BaseUserAdmin):
    """
    Register your models here.
    """
    ordering: Optional[Sequence[str]] = ('email', )
    fieldsets = (
        (None, {'fields': ('nickname', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'phone', 'nickname', 'name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'phone', 'nickname', 'email')


# admin.site.unregister(User)
admin.site.register(models.User, UserAdmin)
