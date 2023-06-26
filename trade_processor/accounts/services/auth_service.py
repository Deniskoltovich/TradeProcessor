from datetime import datetime, timedelta

import jwt
from accounts.models import User
from config import settings
from django.contrib.auth import authenticate


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

        user = authenticate(request, username=username, password=password)
        if user:
            token = jwt.encode(
                {'username': username}, settings.SECRET_KEY, algorithm='HS256'
            )

            return {'token': token}
        else:
            return None
