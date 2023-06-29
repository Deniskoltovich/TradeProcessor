from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions

from accounts.models import User
from accounts.serializers.user_serializers import ListUserSerializer
from config import settings


class AuthService:
    @staticmethod
    def refresh(request):

        """
        The refresh function is used to refresh the access token.
        The function first retrieves the refresh token from the cookie,
        then decodes it using jwt.decode().

        :param request: Get the username from the request object
        :return: The access token
        """
        refresh_token = request.COOKIES.get(
            'refreshtoken'
        )  # Retrieve refresh token from the cookie

        if not refresh_token:
            raise exceptions.AuthenticationFailed()

        decoded_token = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256']
        )
        username = decoded_token.get('username')

        expiration_time = datetime.utcnow() + timedelta(days=0, minutes=20)
        access_token = jwt.encode(
            {'username': username, 'exp': expiration_time},
            settings.SECRET_KEY,
            algorithm='HS256',
        )

        return {'access_token': access_token}

    @staticmethod
    def login(request):
        """
        The login function is used to authenticate a user.
        It takes in the username and password of the user, and returns
            an access token if successful.

        :param request: Get the username and password from the
            request body
        :return: A dictionary containing the access token and
            refresh token
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'username and password required'
            )

        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        serialized_user = ListUserSerializer(user).data

        access_token = AuthService.generate_access_token(user)
        refresh_token = AuthService.generate_refresh_token(user)
        data = {
            'refresh_token': refresh_token,
            'access_token': access_token,
            'user': serialized_user,
        }
        return data

    @staticmethod
    def authenticate(request):

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

        try:
            user = User.objects.filter(
                username=request.jwt_payload.get('username')
            ).first()
        except AttributeError:
            return None
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return (user, None)

    @staticmethod
    def generate_access_token(user):
        """
        The generate_access_token function takes in a user object and
         returns an access token.
        The expiry time of this token is set to 20 minutes.

        :param user: Get the username of the user that is currently
            logged in
        :return: A jwt that contains the username of the user
        """

        access_token_payload = {
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=0, minutes=20),
            'iat': datetime.utcnow(),
        }
        access_token = jwt.encode(
            access_token_payload, settings.SECRET_KEY, algorithm='HS256'
        )
        return access_token

    @staticmethod
    def generate_refresh_token(user):
        """
        The generate_refresh_token function generates a refresh token
         for the user.
        The function takes in a user object and returns the refresh
         token.


        :param user: Get the username of the user
        :return: A refresh token
        """
        refresh_token_payload = {
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow(),
        }
        refresh_token = jwt.encode(
            refresh_token_payload, settings.SECRET_KEY, algorithm='HS256'
        )
        return refresh_token
