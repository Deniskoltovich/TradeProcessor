from accounts.models import User
from accounts.serializers.user_serializers import (
    UpdateUserByAdminSerializer,
)


class UpdateUserByAdminService:
    @staticmethod
    def execute(data, pk):

        """
        The execute function updates the user's status, balance or role
            Args:
                data (dict): The request body containing the new values
                 for status, balance and role.

                *args (list): A list of arguments passed to this
                 function by the client.

        :param data: Pass the data to be updated
        :param *args: Pass a variable number of arguments to a function
        :return: A dictionary of the user's information
        """
        user = User.objects.get(pk=pk)
        if not data.get('status'):
            data['status'] = user.status
        if not data.get('balance'):
            data['balance'] = user.balance
        if not data.get('role'):
            data['role'] = user.role
        serializer = UpdateUserByAdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors
