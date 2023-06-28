from django.contrib.auth import logout

from accounts.serializers.user_serializers import PasswordUserSerializer


class UpdateUserPasswordService:
    @staticmethod
    def update(user, request):
        serializer = PasswordUserSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            logout(request)
            return {'status': 'password set'}
        return serializer.errors
