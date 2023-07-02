from django.contrib.auth import logout

from accounts.serializers.user_serializers import PasswordUserSerializer
from accounts.tasks.send_notification_password_changed import (
    send_notification_about_changed_password,
)


class UpdateUserPasswordService:
    @staticmethod
    def update(user, request):
        serializer = PasswordUserSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            send_notification_about_changed_password.delay(user.id)
            logout(request)
            return {'status': 'password set'}
        return serializer.errors
