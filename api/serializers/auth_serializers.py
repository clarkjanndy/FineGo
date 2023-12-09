from django.contrib.auth.hashers import make_password, check_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from api.models import User
from .extras import CustomModelSerializer, CustomSerializer

__all__ = ['RegistrationSerializer', 'LoginSerializer', 'ChangePasswordSerializer']

class RegistrationSerializer(CustomModelSerializer):

    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff', 'last_login', 'is_active', 'groups', 'user_permissions', 'role')
        read_only_fields = ('date_joined', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # hash the password first
        hashed_password = make_password(validated_data['password'])
        validated_data.update({"password": hashed_password})
                
        return super().create(validated_data)

class LoginSerializer(CustomSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(CustomModelSerializer):
    # the password that we need to validate
    current_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('current_password', 'password')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.instance
        current_password = attrs.get('current_password')

        password_match = check_password(current_password, user.password)
        if not password_match:
            raise ValidationError({"current_password": 'Invalid password.'})
        
        return attrs
    
    def update(self, instance, validated_data):
        # hash the password first
        hashed_password = make_password(validated_data['password'])
        validated_data.update({"password": hashed_password})

        return super().update(instance, validated_data)