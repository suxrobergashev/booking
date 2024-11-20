from authentication.models import User
from utils.get_user_token import decode_jwt_token


def get_role(token):
    return decode_jwt_token(token.split()[1]).get('role', '')


def validate_token(token):
    if token is None:
        return
    if len(token.split()) < 2 or token.split()[0] != "Bearer":
        return
    if decode_jwt_token(token.split()[1]) is None:
        return
    user_id = decode_jwt_token(token.split()[1]).get('user_id', None)
    login_time = decode_jwt_token(token.split()[1]).get('login_time', None)
    if login_time is None or user_id is None:
        return
    if User.objects.filter(id=user_id, login_time=login_time).exists():
        return decode_jwt_token(token.split()[1])
    return
