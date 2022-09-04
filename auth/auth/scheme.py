from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class SimpleJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework_simplejwt.authentication.JWTAuthentication'  # full import path OR class ref
    name = 'simpleJWTAuthentication'  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'description': _(
                'JWT-based authentication with required prefix "%s"'
            ) % "Bearer"
        }
