from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


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


class TestAccessToken(AccessToken):
    """
    Test 시 lifetime을 독립적으로 자유롭게 수정
    """
    pass


class TestRefreshToken(RefreshToken):
    """
    Test 시 lifetime을 독립적으로 자유롭게 수정
    """
    access_token_class = TestAccessToken
