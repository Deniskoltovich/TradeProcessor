from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from accounts.services.auth_service import AuthService


class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(
            lambda: self.__class__.get_user(request)
        )

    @staticmethod
    def get_user(request):
        return AuthService.authenticate_user(request.headers)
