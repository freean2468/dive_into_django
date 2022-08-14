from audioop import reverse
from django.test import TestCase
from .models import User
from rest_framework import status
from django.urls import reverse

# a separate TestClass for each model or view
# a separate test method for each set of conditions you want to test
# test method names that describe their function
class UserTests(TestCase):
    def until_sending_authcode_for_signup(self, p='01079978395'):
        return self.client.post(reverse('users:signup_auth'), {'phone': p})


    def until_authenticating_before_signup(self, p='01079978395', c='150805'):
        self.until_sending_authcode_for_signup()
        return self.client.get(reverse('users:signup_auth'), {'phone': p, 'code': c})


    def until_signup(self, p='01079978395', email='freean2468@gmail.com', nickname='neil', password='1111', name='송훈일'):
        self.until_authenticating_before_signup()
        return self.client.post(reverse('users:signup'), {'email': email, 'nickname': nickname, 'password': password, 'name': name, 'phone': p})


    def until_signin_by_email(self, id='freean2468@gmail.com', password='1111'):
        self.until_signup()
        return self.client.get(reverse('users:signin'), {'id': id, 'password': password})

    
    def until_signin_by_nickname(self, id='neil', password='1111'):
        self.until_signup()
        return self.client.get(reverse('users:signin'), {'id': id, 'password': password})

    
    def until_signin_by_phone(self, id='01079978395', password='1111'):
        self.until_signup()
        return self.client.get(reverse('users:signin'), {'id': id, 'password': password})


    def until_sending_authcode_for_password(self, p='01079978395'):
        return self.client.post(reverse('users:password_auth'), {'phone': p})


    def until_authenticating_before_password(self, p='01079978395', c='150805'):
        self.until_sending_authcode_for_password()
        return self.client.get(reverse('users:password_auth'), {'phone': p, 'code': c})


    def until_password(self, p='01079978395', password='1111'):
        self.until_authenticating_before_password()
        return self.client.post(reverse('users:password'), {'password': password, 'phone': p})


    # def test_detail(self):


    def test_sending_authcode_for_signup(self):
        """
        인증코드를 SMS로 '전송한다고 가정' => 204
        """
        response=self.until_sending_authcode_for_signup()
        self.assertIs(response.status_code, status.HTTP_204_NO_CONTENT)

        # 세션 삭제


    def test_sending_authcode_for_signup_with_invalid_phone_number_places(self):
        """
        유효한 자릿수가 아니면 => 400
        """
        response=self.until_sending_authcode_for_signup('0107997895')
        self.assertIs(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_sending_authcode_for_signup_with_invalid_phone_character(self):
        """
        digit 외의 문자가 섞여 있으면 => 400
        """
        response=self.until_sending_authcode_for_signup('010a9978395')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticationg_before_signup(self):
        """
        valid phone and code => 200
        """
        response=self.until_authenticating_before_signup()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 세션 삭제


    def test_authenticating_before_signup_with_invalid_phone_character(self):
        """
        phone에 digit 외 문자 => 400
        """
        response=self.until_authenticating_before_signup(p='01079*78395')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_signup_with_invalid_phone_places(self):
        """
        phone 유효하지 않은 자릿수 => 400
        """
        response=self.until_authenticating_before_signup(p='0107997835')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_signup_with_invalid_phone_session(self):
        """
        등록된 세션이 없는 phone => 400
        """
        response=self.until_authenticating_before_signup(p='01059978395')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_signup_with_invalid_code(self):
        """
        틀린 인증 코드 => 400
        """
        response=self.until_authenticating_before_signup(c='000000')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_signup_with_invalid_code_places(self):
        """
        code가 요구하는 자릿수가 아닌 경우 => 400
        """
        response=self.until_authenticating_before_signup(c='00000')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_signup_with_invalid_code_character(self):
        """
        code에 digit 외의 문자가 섞여 있으면 => 400
        """
        response=self.until_authenticating_before_signup(c='00a000')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_signup(self):
        # 패스워드 암호화
        """
        유효한 phone session으로 요청 => 201
        """
        response=self.until_signup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_signup_with_invalid_phone(self):
        """
        등록된 세션이 없는 phone => 400
        """
        response=self.until_signup(p='01077114923')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_signup_with_invalid_email(self):
        """
        email 형식이 아닌 email => 400
        """
        response=self.until_signup(email='freean2468gmail.com')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_signup_with_too_long_email(self):
        """
        너무 긴 email => 400
        """
        response=self.until_signup(email='blahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblah@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_signup_with_too_long_nickname(self):
        """
        너무 긴 nickname => 400
        """
        response=self.until_signup(nickname='blahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblah')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_signup_with_too_long_password(self):
        """
        너무 긴 password => 400
        """
        response=self.until_signup(password='blahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblah')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_signup_with_too_long_name(self):
        """
        너무 긴 name => 400
        """
        response=self.until_signup(name='blahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblah')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_signup_with_invalid_phone_places(self):
        """
        요구되는 자릿수가 맞지 않는 phone => 400
        """
        response=self.until_signup(p='010799783957')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_signup_with_duplicated_email(self):
        """
        중복되는 email 요청 => 409
        """
        self.until_signup()
        response=self.until_signup(nickname="other", p="01028398271")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    
    def test_signup_with_duplicated_nickname(self):
        """
        중복되는 nickname 요청 => 409
        """
        self.until_signup()
        response=self.until_signup(email="other@gmail.com", p="01028398271")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    
    def test_signup_with_duplicated_phone(self):
        """
        중복되는 phone 요청 => 409
        """
        self.until_signup()
        response=self.until_signup(email="other@gmail.com", nickname="other")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_signin_by_email(self):
        """
        가입한 email 요청 => 200
        """
        response=self.until_signin_by_email()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_signin_by_email_with_wrong_password(self):
        """
        가입된 email, 잘못된 비밀번호 => 403
        """
        response=self.until_signin_by_email(password='1234')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_signin_by_nickname(self):
        """
        가입한 nickname 요청 => 200
        """
        response=self.until_signin_by_nickname()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_signin_by_nickname_with_wrong_password(self):
        """
        가입된 nickname, 잘못된 비밀번호 => 403
        """
        response=self.until_signin_by_nickname(password='1234')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_signin_by_phone(self):
        """
        가입한 phone 요청 => 200
        """
        response=self.until_signin_by_phone()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_signin_by_phone_with_wrong_password(self):
        """
        가입된 phone, 잘못된 비밀번호 => 403
        """
        response=self.until_signin_by_phone(password='1234')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_signin_with_not_existing_email(self):
        """
        가입하지 않은 email 요청 => 400
        """
        response=self.until_signin_by_email(id="fr@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_signin_with_not_existing_nickname(self):
        """
        가입하지 않은 nickname 요청 => 400
        """
        response=self.until_signin_by_nickname(id="lien")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_signin_with_not_existing_phone(self):
        """
        가입하지 않은 phone 요청 => 400
        """
        response=self.until_signin_by_phone(id="01088278836")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_sending_authcode_for_password(self):
        """
        인증코드를 SMS로 '전송한다고 가정' => 204
        """
        response=self.until_sending_authcode_for_password()
        self.assertIs(response.status_code, status.HTTP_204_NO_CONTENT)

        # 세션 삭제


    def test_sending_authcode_for_password_with_invalid_phone_number_places(self):
        """
        유효한 자릿수가 아니면 => 400
        """
        response=self.until_sending_authcode_for_password('0107997895')
        self.assertIs(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_sending_authcode_for_password_with_invalid_phone_character(self):
        """
        digit 외의 문자가 섞여 있으면 => 400
        """
        response=self.until_sending_authcode_for_password('010a9978395')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticationg_before_password(self):
        """
        valid phone and code => 200
        """
        response=self.until_authenticating_before_password()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 세션 삭제


    def test_authenticating_before_password_with_invalid_phone_character(self):
        """
        phone에 digit 외 문자 => 400
        """
        response=self.until_authenticating_before_password(p='01079*78395')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_password_with_invalid_phone_places(self):
        """
        phone 유효하지 않은 자릿수 => 400
        """
        response=self.until_authenticating_before_password(p='0107997835')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_password_with_invalid_phone_session(self):
        """
        등록된 세션이 없는 phone => 400
        """
        response=self.until_authenticating_before_password(p='01059978395')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_password_with_invalid_code(self):
        """
        틀린 인증 코드 => 400
        """
        response=self.until_authenticating_before_password(c='000000')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_password_with_invalid_code_places(self):
        """
        code가 요구하는 자릿수가 아닌 경우 => 400
        """
        response=self.until_authenticating_before_password(c='00000')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_authenticating_before_password_with_invalid_code_character(self):
        """
        code에 digit 외의 문자가 섞여 있으면 => 400
        """
        response=self.until_authenticating_before_password(c='00a000')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password(self):
        # 패스워드 암호화
        """
        유효한 phone session으로 요청 => 201
        """
        response=self.until_password()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_password_with_invalid_phone(self):
        """
        등록된 세션이 없는 phone => 400
        """
        response=self.until_password(p='01077114923')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_password_with_too_long_password(self):
        """
        너무 긴 password => 400
        """
        response=self.until_signup(password='blahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblahblah')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_with_invalid_phone_places(self):
        """
        요구되는 자릿수가 맞지 않는 phone => 400
        """
        response=self.until_signup(p='010799783957')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

