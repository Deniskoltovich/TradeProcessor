import jwt
from rest_framework import exceptions, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import (
    IsAdministrator,
    IsAnalyst,
    IsOwner,
    IsUser,
)
from accounts.serializers import user_serializers
from accounts.serializers.user_serializers import (
    UpdateUserByAdminSerializer,
)
from accounts.services import (
    auth_service,
    list_transaction_service,
    subscription_service,
)
from accounts.services.user.change_password import (
    UpdateUserPasswordService,
)
from accounts.services.user.create_user import CreateUserService
from accounts.services.user.update_user import UpdateUserService
from assets.serializers import AssetSerializer
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from orders import serializers


class UserViewSet(
    GetSerializerClassMixin,
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
):

    queryset = User.objects.all()

    serializer_role_action_classes = {
        (User.Role.ADMIN, 'list'): user_serializers.AdminViewUserSerializer,
        (
            User.Role.ADMIN,
            'retrieve',
        ): user_serializers.AdminViewUserSerializer,
        (
            User.Role.USER,
            'retrieve',
        ): user_serializers.UserViewUserSerializer,
        (
            User.Role.ADMIN,
            'list_transactions',
        ): serializers.AdminViewOrderSerializer,
        (User.Role.USER, 'create'): serializers.UserViewOrderSerializer,
    }

    serializer_action_classes = {
        'update': user_serializers.UpdateUserByAdminSerializer,
        'retrieve': user_serializers.UserViewUserSerializer,
        "list_transactions": serializers.UserViewOrderSerializer,
        'create': serializers.AdminViewOrderSerializer,
    }

    permission_action_classes = {
        'list': (IsAdministrator,),
        'retrieve': (IsAdministrator | IsOwner,),
        'update': (IsAdministrator | IsOwner,),
        'create': (AllowAny,),
        'login': (AllowAny,),
        'refresh_token': (AllowAny,),
        'add_subscription': (IsUser,),
        'list_subscription': (IsOwner,),
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
            data = UpdateUserService.update(request.data, kwargs['pk'])
            serializer = UpdateUserByAdminSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

        else:
            user = self.get_object()
            return Response(UpdateUserPasswordService.update(user, request))

    def create(self, request, *args, **kwargs):
        user = CreateUserService.create(request)
        serializer = self.get_serializer_class()(instance=user)
        return Response(
            serializer.data,
            status=201,
        )

    @action(
        detail=True,
        methods=('get',),  # type: ignore
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

        (
            order_transactions,
            auto_order_transactions,
        ) = list_transaction_service.ListTransactionsService.execute(pk)

        orders_data = self.get_serializer_class()(
            order_transactions, many=True
        ).data
        auto_orders_data = self.get_serializer_class()(
            auto_order_transactions, many=True
        ).data
        return Response(
            {'orders': orders_data, 'auto_orders': auto_orders_data}
        )

    @action(
        detail=False,
        methods=('get',),  # type: ignore
        url_path='refresh',
    )
    def refresh_token(self, request):
        try:
            return Response(auth_service.AuthService.refresh(request))
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
        methods=('post',),  # type: ignore
        url_path='login',
    )
    def login(self, request):
        access_token, refresh_token = auth_service.AuthService.login(request)
        data = {
            'refresh_token': refresh_token,
            'access_token': access_token,
        }
        return Response(data)

    @action(
        detail=True, methods=('get',), url_path='subscriptions'  # type: ignore
    )
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
            AssetSerializer(request.user.subscriptions, many=True).data
        )

    @list_subscription.mapping.post
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
        subs = subscription_service.SubscriptionService().add(
            request.user, request.data.get('asset_id')
        )
        serializer = AssetSerializer(subs, many=True)
        return Response(serializer.data)

    @list_subscription.mapping.delete
    def delete_subscription(self, request, pk):
        subs = subscription_service.SubscriptionService().delete(
            request.user, request.data.get('asset_id')
        )
        serializer = AssetSerializer(subs, many=True)
        return Response(serializer.data)
