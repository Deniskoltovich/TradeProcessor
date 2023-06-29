from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
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

        username = AuthService.get_username_from_token(refresh_token)

        return {'access_token': AuthService.generate_access_token(username)}

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
        if not username or not password:
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
    def authenticate_user(headers: dict):
        user = AnonymousUser()
        auth_header = headers.get('Authorization', '').split()
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            try:
                username = AuthService.get_username_from_token(auth_header[1])
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Token expired')
            except (jwt.DecodeError, User.DoesNotExist):
                raise exceptions.AuthenticationFailed('Invalid token')

            user = User.objects.get(username=username)

        return user

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
        return AuthService.encode_token(
            user.username, timedelta(days=0, minutes=20)
        )

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

        return AuthService.encode_token(user.username, timedelta(days=7))

    @staticmethod
    def encode_token(username: str, time_delta: timedelta):

        """
        The encode_token function takes in a username and a timedelta
        object.
        It then creates a token payload dictionary with the username,
         an expiration time, and an issued at time. It then encodes
          this payload into JSON Web Token format using the HS256
           algorithm and returns it.

        :param username: str: Pass in the username of the user who is
            logging in
        :param time_delta: timedelta: Set the expiration time of the
            token
        :return: A token
        """
        token_payload = {
            'username': username,
            'exp': datetime.utcnow() + time_delta,
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    @staticmethod
    def get_username_from_token(token: str):
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256']
        )
        return decoded_token.get('username')
