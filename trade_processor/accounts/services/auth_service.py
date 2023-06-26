from datetime import datetime, timedelta

import jwt
from accounts.models import User
from accounts.serializers import ListUserSerializer
from accounts.utils import token_gen
from config import settings
from django.contrib.auth import authenticate
from rest_framework import exceptions


class AuthService:
    @staticmethod
    def refresh(request):
        username = request.user.username

        current_token = request.headers.get('Authorization', '').split()[1]
        try:
            jwt.decode(
                current_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            expiration_time = datetime.utcnow() + timedelta(days=7)
            token = jwt.encode(
                {'username': username, 'exp': expiration_time},
                settings.SECRET_KEY,
                algorithm='HS256',
            )

            return {'token': token}

        return {'token': current_token}

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
