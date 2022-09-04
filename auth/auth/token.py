from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @extend_schema(tags=['token'])
    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)


class MyTokenRefreshView(TokenRefreshView):
    @extend_schema(tags=['token'])
    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)
