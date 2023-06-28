import jwt
from rest_framework import exceptions, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.authentication import JWTAuthentication
from accounts.models import User
from accounts.permissions import (
    IsAdministrator,
    IsAnalyst,
    IsOwner,
    IsUser,
)
from accounts.serializers import user_serializers
from accounts.services import (
    auth_service,
    list_transaction_service,
    subscription_service,
)
from accounts.services.user_services import create_user_service
from accounts.services.user_services import (
    update_user_by_admin_service as admin_update,
)
from accounts.services.user_services import (
    update_user_password_service as password_update,
)
from mixins.get_serializer_class_mixin import GetSerializerClassMixin


class UserViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    GetSerializerClassMixin,
):
    authentication_classes = [JWTAuthentication]

    queryset = User.objects.all()
    serializer_class = user_serializers.ListUserSerializer

    serializer_action_classes = {
        'update': user_serializers.UpdateUserByAdminSerializer,
        'create': user_serializers.CreateUserSerializer,
    }
    permission_action_classes = {
        'list': (IsAdministrator,),
        'retrieve': (IsAdministrator | IsOwner,),
        'update': (IsAdministrator | IsOwner,),
        'create': (AllowAny,),
        'login': (AllowAny,),
        'refresh_token': (AllowAny,),
        'add_subscription': (IsUser,),
        'list_subscription': (IsUser,),
        'delete_subscription': (IsOwner,),
        'list_transactions': (IsAdministrator | IsOwner | IsAnalyst,),
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (IsUser,)
            )
        ]

    def update(self, request, *args, **kwargs):

        """
        The update function is used to update a user's information.
        If a user is not an admin, they can only edit their own profile
        The update method from user is used to change password.
        If request.user is superuser, he can change user balance,
         status and role

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument
            list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
            to a function
        :return: A response object
        """
        if request.user.role == User.Role.ADMIN:
            return Response(
                admin_update.UpdateUserByAdminService().execute(
                    request.data, kwargs['pk']
                )
            )
        else:
            user = self.get_object()
            return Response(
                password_update.UpdateUserPasswordService().execute(
                    user, request
                )
            )

    def create(self, request, *args, **kwargs):
        return Response(
            create_user_service.CreateUserService().execute(request),
            status=201,
        )

    @action(
        detail=True,
        methods=['get'],
        url_path='transactions',
    )
    def list_transactions(self, request, pk):

        """
        The list_transactions function is used to list all
         transactions for a given account.
        It takes in the request and pk (primary key) of the account,
         and returns a response containing
        all transactions associated with that account.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param pk: Retrieve the transactions of a specific account
        :return: A list of transactions' data
        """
        return Response(
            list_transaction_service.ListTransactions().execute(pk)
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='refresh_token',
    )
    def refresh_token(self, request):
        try:
            return Response(auth_service.AuthService().refresh(request))
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token expired'}, status=401)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=401)
        except exceptions.AuthenticationFailed:
            return Response(
                {'error': 'Refresh token is not provided'}, status=401
            )

    @action(
        detail=False,
        methods=['post'],
        url_path='login',
        permission_classes=[AllowAny],
    )
    def login(self, request):

        data = auth_service.AuthService().login(request)
        response = Response()
        response.set_cookie(
            key='refreshtoken', value=data.get('refresh_token'), httponly=True
        )
        response.data = {
            'access_token': data.get('access_token'),
            'user': data.get('serialized_user'),
        }
        return response

    @action(
        detail=True,
        methods=['post'],
        url_path='subscriptions/add',
    )
    def add_subscription(self, request, pk):

        """
        The add_subscription function is used to add a subscription
         for the user.

        :param self: Represent the instance of the class
        :param request: Get the user and asset_id from the request
        :param pk: Get the primary key of the asset that is being
            subscribed to
        :return: A response object
        """
        return Response(
            subscription_service.SubscriptionService().add(
                request.user, request.data.get('asset_id')
            )
        )

    @action(detail=True, methods=['get'], url_path='subscriptions')
    def list_subscription(self, request, pk=None):

        """
        The list_subscription function is used to list all the
         subscriptions of a user.

        :param self: Represent the instance of the object itself
        :param request: Get the user from the request object
        :param pk: Get the primary key of the object
        :return: A list of all the subscriptions for a user
        """
        return Response(
            subscription_service.SubscriptionService().list(request.user)
        )

    @action(
        detail=True,
        methods=['DELETE'],
        url_path='subscriptions/delete',
    )
    def delete_subscription(self, request, pk):

        return Response(
            subscription_service.SubscriptionService().delete(
                request.user, request.data.get('asset_id')
            )
        )
