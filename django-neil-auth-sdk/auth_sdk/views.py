from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from auth_sdk.authentication import get_permission_data


class DetailPermission(BasePermission):
    def has_permission(self, request, view):
        permission_data = get_permission_data(
            request,
            ''
        )
        print('hi : {permission_data}')
        return "detail" in permission_data.get("permission")


# Create your views here.
@extend_schema(
    tags=["user"],
    summary="user 정보",
    description='header Authorization에 Token token 형식으로 요청하면 해당 토큰으로 식별 가능한 유저 정보 반환',
    responses={
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description='틀린 토큰 or Authorization field가 없을 때',
        ),
        status.HTTP_200_OK: OpenApiResponse(
            description='user의 email, phone, nickname, name',
        )
    },
)
@api_view(['GET'])
@permission_classes([DetailPermission])
def users_detail(request):
    return Response({
        "email": request.user.email,
        "phone": request.user.phone,
        "nickname": request.user.nickname,
        "name": request.user.name
    }, status=status.HTTP_200_OK)
