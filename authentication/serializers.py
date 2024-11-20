from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, Otp
from .utils import validate_uz_number


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class ResponseUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=14)


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('id', 'otp_key', 'otp_code')


class ResponseOtpSerializer(serializers.Serializer):
    otp_code = serializers.IntegerField(
        min_value=100000,
        max_value=999999,
    )
    otp_key = serializers.UUIDField()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[validate_uz_number], max_length=14)
    password = serializers.CharField(max_length=255)
