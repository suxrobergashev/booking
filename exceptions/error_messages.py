from enum import Enum

from rest_framework import status


class ErrorCodes(Enum):
    UNAUTHORIZED = 1
    INVALID_INPUT = 2
    FORBIDDEN = 3
    NOT_FOUND = 4
    ATTEMPT_ALREADY_EXISTS = 5
    ALREADY_EXISTS = 6
    USER_DOES_NOT_EXIST = 7
    INCORRECT_PASSWORD = 8
    INVALID_TOKEN = 9
    EXPIRED_TOKEN = 10
    VALIDATION_FAILED = 11
    USER_BLOCKED = 12
    NOT_EXPIRED = 13


error_messages = {
    1: {"result": "Unauthorized access", "http_status": status.HTTP_401_UNAUTHORIZED},
    2: {"result": "Invalid input provided", "http_status": status.HTTP_400_BAD_REQUEST},
    3: {"result": "Permission denied", "http_status": status.HTTP_403_FORBIDDEN},
    4: {"result": "Resource not found", "http_status": status.HTTP_404_NOT_FOUND},
    5: {"result": "You already have 3 attempts, please return after 12 times",
        "http_status": status.HTTP_400_BAD_REQUEST},
    6: {"result": "User Already exists", "http_status": status.HTTP_400_BAD_REQUEST},
    7: {"result": "User Does not exist", "http_status": status.HTTP_400_BAD_REQUEST},
    8: {"result": "Incorrect password", "http_status": status.HTTP_400_BAD_REQUEST},
    9: {"result": "Invalid Token", "http_status": status.HTTP_400_BAD_REQUEST},
    10: {"result": "Token Expired", "http_status": status.HTTP_400_BAD_REQUEST},
    11: {"result": "Validate Error", "http_status": status.HTTP_400_BAD_REQUEST},
    12: {'result': "User blocked", "http_status": status.HTTP_400_BAD_REQUEST},
    13: {"result": "Otp not expired", "http_status": status.HTTP_400_BAD_REQUEST},
}


def get_error_message(code):
    return error_messages.get(code, 'Unknown error')
