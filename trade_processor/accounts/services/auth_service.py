from datetime import datetime, timedelta

import jwt
from rest_framework import exceptions

from accounts.models import User
from accounts.serializers import ListUserSerializer
from accounts.utils import token_gen
from config import settings


class AuthService:
    @staticmethod
    def refresh(request):
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

        access_token = token_gen.generate_access_token(user)
        refresh_token = token_gen.generate_refresh_token(user)
        data = {
            'refresh_token': refresh_token,
            'access_token': access_token,
            'user': serialized_user,
        }
        return data
