import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):

        """
        The authenticate function is called on every request,
            if the endpoint requires authentication.
        The purpose of the function is to authenticate the user for
            each request. If authentication succeeds, a two-tuple of
        (user, token) is returned. If not, None is returned.

        :param self: Refer to the class itself
        :param request: Get the authorization header from the request
        :return: A tuple of (user, token)
        """

        User = get_user_model()

        if request.path.endswith('/login/'):
            return None

        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        user = User.objects.filter(username=payload['username']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return (user, None)
