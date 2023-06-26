import jwt
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Method used to check authentication for a user by JWT
        """
        # Skip JWT verification for specific paths
        if (
            request.path_info
            in [
                '/accounts/users/',
                '/accounts/users/login/',
                '/accounts/users/refresh_token/',
                '/api/doc/',
                reverse('admin:index'),
                reverse('admin:login'),
            ]
            or request.user.is_superuser
        ):
            return self.get_response(request)

        # Get the JWT token from the request headers
        auth_header = request.headers.get('Authorization', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return JsonResponse(
                {'error': 'Invalid authorization header'}, status=401
            )

        token = auth_header[1]

        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256']
            )
            request.jwt_payload = decoded_token
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return self.get_response(request)
