import uuid

from django.db import models

from abstraction.base_model import BaseModel
from .utils import validate_uz_number


class User(BaseModel):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14, validators=[validate_uz_number])
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Otp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    otp_code = models.IntegerField()
    otp_key = models.CharField(default=uuid.uuid4, max_length=200, editable=False, unique=True)
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'
