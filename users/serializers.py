from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
import re

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):

    # defines the metadata information that our model has (database) and that must be converted to the User class.
    class Meta:
        model = User
        fields = ('pk', 'email', 'nickname', 'password', 'name', 'phone', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AuthSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=11, max_length=11)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_phone(self, value):
        m = re.search(r'(?!([0-9])).', value)
        if m:
            raise serializers.ValidationError("phone should only contain numeric characters")
        return value

    def validate_code(self, value):
        m = re.search(r'(?!([0-9])).', value)
        if m:
            raise serializers.ValidationError("code should only contain numeric characters")
        return value


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=11, max_length=11)

    def validate_phone(self, value):
        m = re.search(r'(?!([0-9])).', value)
        if m:
            raise serializers.ValidationError("phone should only contain numeric characters")
        return value


class SigninSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()


class SignupPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=24)


class PasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=11, max_length=11)
    prior = serializers.CharField(min_length=8, max_length=24)
    new = serializers.CharField(min_length=8, max_length=24)

    def validate_phone(self, value):
        m = re.search(r'(?!([0-9])).', value)
        if m:
            raise serializers.ValidationError("phone should only contain numeric characters")
        return value

