from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view, OpenApiParameter, inline_serializer  # noqa
from auth.token import get_tokens_for_user
from .errors import Errors, ec
from .models import User
from .serializers import PasswordSerializer, AuthSerializer, PhoneSerializer, SigninSerializer, SignupPasswordSerializer, UserSerializer  # noqa
from .cache import AUTH_TIMEOUT, PASSWORD_TIMEOUT, SIGNUP_TIMEOUT, make_key_for_password, make_key_for_password_auth, make_key_for_signup, make_key_for_signup_auth  # noqa

"""
Each view is responsible for doing one of two things:
Returning an HttpResponse object containing the content for the requested page,
or raising an exception such as Http404.
"""

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@extend_schema(
    tags=["user"],
    summary="user 정보",
    description='access 토큰으로 식별된 유저 정보 반환',
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@cache_page(CACHE_TTL)
def users_detail(request: Request):
    return Response({
        "email": request.user.email,
        "phone": request.user.phone,
        "nickname": request.user.nickname,
        "name": request.user.name
    }, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        tags=["user"],
        summary="회원가입 전 인증코드 확인",
        description='전달받은 인증코드가 일치하는지 유효한지 확인 후 회원가입 세션 생성',
        parameters=[
            OpenApiParameter(name='phone', description="11자의 핸드폰 숫자"),
            OpenApiParameter(name='code', description="6자의 숫자")
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='인증 완료',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='입력된 데이터의 길이, 값 불량',
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='이전 인증 절차가 없는 접근',
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
                description='인증 코드가 틀림',
            )
        },
    ),
    post=extend_schema(
        tags=["user"],
        summary="회원가입 전 인증코드 전송",
        description='회원가입 전 인증코드를 유저 phone SMS로 전송',
        request=PhoneSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='전송 완료',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='입력된 데이터의 길이, 값 불량',
            ),
        },
    ),
)
@api_view(['GET', 'POST'])
def users_signup_auth(request: Request):
    if request.method == 'GET':
        serializer = AuthSerializer(
            data={
                'phone': request.GET.get('phone'),
                'code': request.GET.get('code')
            }
        )
        serializer.is_valid(raise_exception=True)

        code = cache.get(make_key_for_signup_auth(serializer.data['phone']) or '')

        if not code:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if code != int(serializer.data['code']):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        cache.delete(make_key_for_signup_auth(serializer.data['phone']))
        cache.set(make_key_for_signup(
            serializer.data['phone']),
            serializer.data['phone'],
            SIGNUP_TIMEOUT
        )

        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        """
        유저 핸드폰으로 회원가입용 인증 코드를 전송(했다고 가정하고) 후 세션 생성
        인증코드는 150805(라고 가정)

        throttling을 적용해야
        """
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cache.set(make_key_for_signup_auth(serializer.data['phone']), 150805, AUTH_TIMEOUT)

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["user"],
    summary="회원가입",
    description="""phone : 11자의 핸드폰 숫자 </br>
                email : 62bytes 이하의 이메일 </br>
                nickname : 16bytes 이하의 닉네임 </br>
                name : 32bytes 이하의 본명 </br>
                password : 8bytes 이상 24bytes 이하의 비밀번호""",
    request=UserSerializer,
    responses={
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description='description에 명시된 필드가 입력되지 않거나 값이 유효하지 않을 때, 중복일 때',
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description='핸드폰 인증이 안 된 접근',
        ),
        status.HTTP_201_CREATED: OpenApiResponse(
            description='회원가입 완료',
        )
    },
)
@api_view(['POST'])
def users_signup(request: Request):
    password_serializer = SignupPasswordSerializer(data={'password': request.data['password']})
    password_serializer.is_valid(raise_exception=True)

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = request.data['phone']
    p = cache.get(make_key_for_signup(phone))
    if not p:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer.save()

    cache.delete(make_key_for_signup(phone))

    return Response(status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["user"],
    summary="로그인",
    description='id(email, phone, nickname 중 하나) + password 로 로그인',
    request=SigninSerializer,
    responses={
        status.HTTP_200_OK: inline_serializer(
            name="authenticated",
            fields={
                'access': serializers.CharField(),
                'refresh': serializers.CharField(),
            }
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description='필드 입력 값이 없을 때',
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            description='ID에 대한 Password가 틀렸을 때',
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description='유효한 ID가 없을 때',
        )
    },
)
@api_view(['POST'])
def users_signin(request: Request):
    serializer = SigninSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    queryset = (
        User.objects.filter(email=serializer.data['id'])
        | User.objects.filter(phone=serializer.data['id'])
        | User.objects.filter(nickname=serializer.data['id'])
    )

    if not queryset:
        return Response(ec(Errors.SIGNIN_NOT_VALID_ID), status=status.HTTP_404_NOT_FOUND)

    user = None
    for q in queryset:
        if check_password(request.data['password'], q.password):
            user = q
            break

    if user is None:
        return Response(ec(Errors.SIGNIN_NOT_VALID_PASSWORD), status=status.HTTP_403_FORBIDDEN)

    return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        tags=['user'],
        summary='비밀번호 재설정 전 인증코드 확인',
        description='전달받은 인증코드가 일치하는지 유효한지 확인 후 비밀번호 세션 생성',
        parameters=[
            OpenApiParameter(name='phone', description="11자의 핸드폰 숫자"),
            OpenApiParameter(name='code', description="6자의 숫자")
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='인증 완료',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='입력된 데이터의 길이, 값 불량',
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description='이전 인증 절차가 없는 접근',
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
                description='인증 코드가 틀림',
            )
        },
    ),
    post=extend_schema(
        tags=['user'],
        summary='비밀번호 재설정 전 인증코드를 유저의 핸드폰으로 SMS 전송',
        description='phone : 유저의 11자리 핸드폰 번호',
        request=PhoneSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description='전송 완료',
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='입력된 데이터의 길이, 값 불량',
            ),
        },
    ),
)
@api_view(['GET', 'POST'])
def users_password_auth(request: Request):
    if request.method == 'GET':
        """
        전달받은 인증코드가 일치하는지 유효한지 확인 후 비밀번호 세션 생성
        """
        serializer = AuthSerializer(
            data={
                'phone': request.GET.get('phone'),
                'code': request.GET.get('code')
            }
        )

        serializer.is_valid(raise_exception=True)

        code = cache.get(make_key_for_password_auth(serializer.data['phone']))

        if not code:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if code != int(request.GET.get('code')):
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        cache.delete(make_key_for_password_auth(serializer.data['phone']))
        cache.set(make_key_for_password(serializer.data['phone']), True, PASSWORD_TIMEOUT)

        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        """
        유저 핸드폰으로 비밀번호 인증 코드를 전송(했다고 가정하고) 후 세션 생성
        인증코드는 150805(라고 가정)
        """
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        get_object_or_404(User, phone=serializer.data['phone'])

        cache.set(make_key_for_password_auth(serializer.data['phone']), 150805, AUTH_TIMEOUT)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["user"],
    summary="비밀번호 재설정",
    description="""phone : 11자의 핸드폰 번호</br>
                new : 새로운 비밀번호""",
    request=PasswordSerializer,
    responses={
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            description='비밀번호 재설정 완료',
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description='이전 인증 절차가 없는 접근',
        ),
    },
)
@api_view(['PATCH'])
def users_password(request: Request):
    serializer = PasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    flag = cache.get(make_key_for_password(serializer.data['phone']))

    if flag is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.get(phone=serializer.data['phone'])

    user.set_password(serializer.data['new'])
    user.save()

    cache.delete(make_key_for_password(serializer.data['phone']))

    return Response(status=status.HTTP_204_NO_CONTENT)
