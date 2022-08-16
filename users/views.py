from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .error_codes import ErrorCodes

from .models import User
from .serializers import UserSerializer

# Each view is responsible for doing one of two things: 
# Returning an HttpResponse object containing the content for the requested page, 
# or raising an exception such as Http404.

def ec(error_code):
    return { 'error_code': error_code }

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def users_detail(request):
    print(request.user)
    print(request.auth)

    # 내 정보보기 기능
    return Response({
        "email": request.user.email,
        "phone": request.user.phone,
        "nickname": request.user.nickname,
        "name": request.user.name
    },status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def users_signup_auth(request):
    if request.method == 'GET':
        """
        전달받은 인증코드가 일치하는지 유효한지 확인 후 회원가입 세션 생성
        """
        # print(request.GET.get('code', 0))
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        """
        유저 핸드폰으로 회원가입용 인증 코드를 전송(했다고 가정하고) 후 세션 생성
        인증코드는 150805(라고 가정)
        """
        # print(request.POST.get('phone', 0))
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
회원가입
"""
@api_view(['POST'])
def users_signup(request):
    # print('request.POST.get : %s' % request.POST.get('phone', '0'))
    # print('request.data : %s' % request.data)
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        # user = serializer.Meta.model
        # print(user)
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
로그인
email, phone, nickname으로 로그인이 가능해야 함. (모두 중복될 수 없음)
"""
@api_view(['POST'])
def users_signin(request):
    print(request.data)

    try:
        id, password = request.data['id'], request.data['password']
    except KeyError:
        return Response(ec(ErrorCodes.SIGNIN_LACK_OF_POST_DATA.value), status=status.HTTP_400_BAD_REQUEST)

    queryset = User.objects.filter(email=id) | User.objects.filter(phone=id) | User.objects.filter(nickname=id)

    print('queryset : %s' % queryset)

    if not queryset:
        return Response(ec(ErrorCodes.SIGNIN_NOT_VALID_ID.value), status=status.HTTP_404_NOT_FOUND)

    user = None
    for q in queryset:
        if q.password == password:
            user = q
            break

    if user is None:
        return Response(ec(ErrorCodes.SIGNIN_NOT_VALID_PASSWORD.value), status=status.HTTP_403_FORBIDDEN)

    token, created = Token.objects.get_or_create(user=user)

    return Response({ 'token': token.key }, status=status.HTTP_200_OK)


"""
핸드폰에 비밀번호 찾기용 인증 코드 전송(했다고 가정하고) 후 세션 생성
인증코드는 150805(라고 가정)
"""
@api_view(['GET', 'POST'])
def users_password_auth(request):
    if request.method == 'GET':
        """
        전달받은 인증코드가 일치하는지 유효한지 확인 후 비밀번호 세션 생성
        """
        # print(request.GET.get('code', 0))
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        """
        유저 핸드폰으로 비밀번호 인증 코드를 전송(했다고 가정하고) 후 세션 생성
        인증코드는 150805(라고 가정)
        """
        # print(request.POST.get('phone', 0))
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
인증코드 확인 후 비밀번호 재설정 세션 생성
"""
@api_view(['PUT'])
def users_password(request):
    return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def users_list(request):
#     if request.method == 'GET':
#         data = User.objects.all()

#         serializer = UserSerializer(data, context={'request': request}, many=True)

#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def users_detail(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     # 내 정보보기 기능
#     if request.method == 'GET':
#         pass
#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)