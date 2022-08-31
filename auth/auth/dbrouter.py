from django.conf import settings


class AuthRouter:
    """
    https://docs.djangoproject.com/en/3.2/topics/db/multi-db/
    """
    def db_for_read(self, model, **hints):
        if model._meta.db_table == settings.AUTH_USER_TABLE:
            return settings.AUTH_DB
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == settings.AUTH_USER_TABLE:
            return False
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.db_table == settings.AUTH_USER_TABLE
                or obj2._meta.db_table == settings.AUTH_USER_TABLE):
            return True
