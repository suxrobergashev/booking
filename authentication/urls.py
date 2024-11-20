from django.urls import path
from .views import UserViewSet, OtpViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='me'),
    path('verify/', OtpViewSet.as_view({'post': 'verify'}), name='verify'),
    path('reset/<uuid:otp_key>/', OtpViewSet.as_view({'get': 'reset_otp'}), name='reset_otp'),
]
