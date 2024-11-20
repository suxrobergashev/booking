from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from utils.chek_token import validate_token


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Target URLs where authentication is needed
        exclude_target_url = [reverse('login'), reverse('register'), reverse('district'), reverse('verify'),
                              reverse('reset_otp')]
        if request.path.startswith('/api/v1/') and request.path not in exclude_target_url:
            # Check token validity
            payload = validate_token(request.headers.get('Authorization'))

            if payload is None:
                return JsonResponse(data={'result': "", "error": "Unauthorized access", 'ok': False}, status=401)
        return None
