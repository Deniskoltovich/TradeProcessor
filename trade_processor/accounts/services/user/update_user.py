from accounts.models import User


class UpdateUserService:
    @staticmethod
    def update(data, pk: int):

        """
        The update function updates the user's status, balance or role
            Args:
                data (dict): The request body containing the new values
                 for status, balance and role.

                pk (int): A primary key passed to this
                 function by the client.

        :param data: Pass the data to be updated
        :param pk: Pass the pk of user to a function
        :return: A dictionary of the user's information
        """
        user = User.objects.get(pk=pk)
        if data.get('balance'):
            data['balance'] += user.balance
        else:
            data['balance'] = user.balance
        if not data.get('status'):
            data['status'] = user.status
        if not data.get('role'):
            data['role'] = user.role

        return data
