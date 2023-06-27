from django.contrib.auth import logout

from accounts import serializers


class UpdateUserService:
    @staticmethod
    def execute(user, request):
        serializer = serializers.PasswordUserSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            logout(request)
            return {'status': 'password set'}
        return serializer.errors
