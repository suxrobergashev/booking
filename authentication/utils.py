import re
import random
from django.core.validators import ValidationError
from django.utils import timezone
from datetime import timedelta, datetime
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException


def validate_uz_number(value):
    if re.match(r'^\+998\d{9}$', value):
        return value
    else:
        raise ValidationError("Iltimos O'zbekiston telefon raqamini kiriting!")




def generate_otp_code():
    return str(random.randint(100000, 999999))

def _generate_otp(user_id: int):
    from .models import Otp
    if user_id is None:
        raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
    otp_code = generate_otp_code()
    otp = Otp.objects.create(user_id=user_id, otp_code=otp_code)
    otp.save()
    return otp


def _check_max_resend_limit(all_otp):
    latest_otp = all_otp.order_by('-created_at').first()
    if len(all_otp) >= 3 and latest_otp.created_at > timezone.now() - timedelta(hours=12):
        raise CustomApiException(
            ErrorCodes.ATTEMPT_ALREADY_EXISTS,
            time=((latest_otp.created_at + timedelta(hours=12))- timezone.now()).total_seconds()
        )

def _max_resend_limit_delete(all_otp, new_otp: str):
    latest_otp = all_otp.order_by('-created_at').exclude(otp_key=new_otp).first()
    if latest_otp and latest_otp.created_at < timezone.now() - timedelta(hours=12) and len(all_otp) >= 2:
        all_otp.exclude(otp_key=new_otp).delete()

def _check_expires_at(first_otp):

    if first_otp and first_otp.created_at + timedelta(minutes=1) > timezone.now():
        remaining_time = (first_otp.created_at + timedelta(minutes=1) - timezone.now()).total_seconds()
        raise CustomApiException(ErrorCodes.NOT_EXPIRED, time=remaining_time)