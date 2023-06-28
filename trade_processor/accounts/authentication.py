from rest_framework.authentication import BaseAuthentication

from accounts.services.auth_service import AuthService


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return AuthService.authenticate(request)
