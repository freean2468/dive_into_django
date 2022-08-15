from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .models import User
from .serializers import UserSerializer

# Each view is responsible for doing one of two things: 
# Returning an HttpResponse object containing the content for the requested page, 
# or raising an exception such as Http404.

class CustomAuthToken(ObtainAuthToken):
    def get(self, request, *args, **kwargs):
        print('in CustomAuthToken : %s' % request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data['user'])
        user = serializer.validated_data['user']
        print(user)
        token, created = Token.objects.get_or_create(user=user)

        print(token)

        print(created)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def users_detail(request):
    print(str(request.user))
    print(str(request.auth))

    try:
        user = User.objects.get(email=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 내 정보보기 기능
    return Response(status=status.HTTP_200_OK)


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
        user = serializer.Meta.model
        token = Token.objects.create(user=user)
        print(token.key)
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
로그인
email, phone, nickname으로 로그인이 가능해야 함. (모두 중복될 수 없음)
"""
@api_view(['GET'])
@schema(CustomAuthToken)
def users_signin(request):
    # id 조회 순서 
    # email -> phone -> nickname
    id = request.GET.get('id', '')
    print('id : %s' % id)

    try:
        user = User.objects.get(email=id)
        print(user)
    except User.DoesNotExist:
        try:
            user = User.objects.get(phone=id)
            print(user)
        except User.DoesNotExist:
            try:
                user = User.objects.get(nickname=id)
                print(user)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(status=status.HTTP_200_OK)


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