from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import BadRequest
from django.urls import reverse
from rest_framework import exceptions

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

        user = get_user_model().objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        access_token = AuthService.generate_access_token(user)
        refresh_token = AuthService.generate_refresh_token(user)
        return access_token, refresh_token

    @staticmethod
    def authenticate_user(headers: dict):
        user = AnonymousUser()
        auth_header = headers.get('Authorization', '').split()
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            try:
                username = AuthService.get_username_from_token(auth_header[1])
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Token expired')
            except (jwt.DecodeError, get_user_model().DoesNotExist):
                raise exceptions.AuthenticationFailed('Invalid token')

            user = get_user_model().objects.get(username=username)

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

    @staticmethod
    def generate_activation_link(user_id):

        """
        The generate_activation_link function takes a user_id as an
         argument and returns a tuple containing the activation link
         and the user object. The function first gets the User model
         from Django's get_user_model() method, then uses that to
         retrieve the user with the given id. Next, it generates a
         confirmation token using Django's default token generator.
         Finally, it creates an activation link by combining
         the reverse of our accounts:users-activate-user URL pattern
         with query parameters for both the user id and confirmation
          token.

        :param user_id: Get the user from the database
        :return: A tuple with the activation link and the user object
        """
        user = get_user_model().objects.get(pk=user_id)
        confirmation_token = default_token_generator.make_token(user)
        activation_link = (
            f'{reverse("accounts:users-activate-user")} + '
            f'?user_id={user_id}&confirmation_token={confirmation_token}'
        )
        return activation_link, user

    @staticmethod
    def activate_user(user_id, confirmation_token):
        """
        The activate_user function is used to activate a user's account.

        :param user_id: Get the user from the database
        :param confirmation_token: Check if the user is valid
        :return: None
        """
        user = get_user_model().get(pk=user_id)

        if not default_token_generator.check_token(user, confirmation_token):
            raise BadRequest

        user.status = user.Status.ACTIVE
        user.save()
