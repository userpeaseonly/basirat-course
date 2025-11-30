from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model
    """
    phone_number = PhoneNumberField()

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'is_student', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users
    """
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'password_confirm', 'first_name', 'last_name', 'is_student']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True)
