from rest_framework import serializers
from .models import User

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):

    # defines the metadata information that our model has (database) and that must be converted to the User class.
    class Meta:
        model = User
        fields = ('pk', 'email', 'nickname', 'password', 'name', 'phone', 'created_at', 'updated_at')