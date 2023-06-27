import jwt

from accounts.models import User
from config import settings


class CreateUserService:
    @staticmethod
    def execute(request):
        username = request.data.get('username')
        password = request.data.pop('password')
        email = request.data.pop('email')
        User.objects.create_user(email, password, **request.data)

        token = jwt.encode(
            {'username': username}, settings.SECRET_KEY, algorithm='HS256'
        )

        return {'token': token}
