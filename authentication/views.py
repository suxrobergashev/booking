from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from .models import User, Otp
from .serializers import UserSerializer, ResponseOtpSerializer, LoginSerializer
from .utils import _check_max_resend_limit, _max_resend_limit_delete, _generate_otp, _check_expires_at


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='User registration',
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'result': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'otp_key': openapi.Schema(type=openapi.TYPE_STRING, description="Otp key")
                        }
                    ),
                }
            ),
        },
        request_body=UserSerializer(),
        tags=['User'],
    )
    def create(self, request):
        data = request.data
        phone_number = data.get('phone_number', '')

        # Check if user exists and is active
        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.is_verified:
            raise CustomApiException(ErrorCodes.ALREADY_EXISTS)

        # Initialize serializer for new or existing user
        serializer = UserSerializer(user, data=data, partial=bool(user))
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        user_id = serializer.instance.id
        all_otp = Otp.objects.filter(user_id=user_id)

        # Check resend limit and generate OTP
        _check_max_resend_limit(all_otp)
        otp = _generate_otp(user_id)
        _max_resend_limit_delete(all_otp, otp.otp_key)

        return Response({'result': {'otp_key': otp.otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='User login',
        request_body=LoginSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'result': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access token"),
                            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token")
                        }
                    ),
                }
            ),
        },
        tags=['User'],
    )
    def login(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        user = User.objects.filter(phone_number=data.get('phone_number', '')).first()
        if not user:
            raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
        print(check_password(data.get('password', ''), user.password))
        print(data.get('password', ''))
        if not check_password(data.get('password', ''), user.password):
            raise CustomApiException(ErrorCodes.INCORRECT_PASSWORD)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response(data={'result': {'access_token': access_token, 'refresh_token': str(refresh)}, 'ok': True},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='User auth me',
        responses={200: UserSerializer()},
        tags=['User'],
    )
    def me(self, request):
        user = User.objects.filter(id=request.user.id).first()
        return Response({'result': UserSerializer(user).data, 'ok': True}, status=status.HTTP_200_OK)


class OtpViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='OTP verify',
        responses={200: "User successfully verified"},
        request_body=ResponseOtpSerializer(),
        tags=['Otp'],
    )
    def verify(self, request):
        data = request.data
        otp_key = data.get('otp_key')
        otp_code = data.get('otp_code')

        # Validate OTP data
        serializer = ResponseOtpSerializer(data=data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        otp = Otp.objects.filter(otp_key=otp_key).first()
        if not otp:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message="OTP does not exist")
        otp.request_count += 1
        otp.save()
        # Verify OTP code and expiration
        if otp.created_at + timedelta(minutes=1) < timezone.now() or otp.request_count >= 3:
            raise CustomApiException(ErrorCodes.INVALID_INPUT,
                                     message="OTP expired or the number of attempts exceeded 3")
        if otp.otp_code != otp_code:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message="OTP code does not match")

        # Verify user and update status
        user = User.objects.filter(id=otp.user_id).first()
        if not user:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message="User does not exist")

        user.is_verified = True
        user.save()
        Otp.objects.filter(user_id=user).delete()

        return Response({'result': "User successfully verified", 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='OTP reset',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'result': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'otp_key': openapi.Schema(type=openapi.TYPE_STRING, description="Otp key")
                        }
                    ),
                }
            ),
        },
        tags=['Otp'],
    )
    def reset_otp(self, request, otp_key):
        otp = Otp.objects.filter(otp_key=otp_key).first()
        if not otp:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message="OTP does not exist")

        _check_expires_at(otp)
        all_otp = Otp.objects.filter(user_id=otp.user_id)
        _check_max_resend_limit(all_otp)
        otp = _generate_otp(otp.user_id)
        _max_resend_limit_delete(all_otp, otp.otp_key)
        return Response({'result': {'otp_key': otp.otp_key}, 'ok': True}, status=status.HTTP_200_OK)
