import jwt

from accounts.models import User
from config import settings


class CreateUserService:
    @staticmethod
    def create(request):
        password = request.data.pop('password')
        email = request.data.pop('email')
        return User.objects.create_user(email, password, **request.data)
