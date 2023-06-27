import jwt
from rest_framework import exceptions, generics, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts import serializers
from accounts.authentication import JWTAuthentication
from accounts.models import Portfolio, User
from accounts.permissions import IsAdministrator, IsAnalyst, IsOwner, IsUser
from accounts.services import (
    auth_service,
    create_user_service,
    list_transaction_service,
    portfolio_service,
    subscription_service,
    update_user_service,
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
    serializer_class = serializers.ListUserSerializer

    serializer_action_classes = {
        "partial_update": serializers.PartialUpdateUserSerializer,
        'update': serializers.PartialUpdateUserSerializer,
        'create': serializers.CreateUserSerializer,
    }
    permission_action_classes = {
        'list': (IsAdministrator,),
        'retrieve': (IsAdministrator | IsOwner,),
        'update': (IsOwner | IsAdministrator,),
        'partial_update': (IsOwner | IsAdministrator,),
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
        if request.user.Role.ADMIN:
            return super().update(request, *args, **kwargs)
        else:
            user = self.get_object()
            return Response(
                update_user_service.UpdateUserService().execute(
                    user, request.data
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
        return Response(
            subscription_service.SubscriptionService().add(
                request.user, request.data.get('asset_id')
            )
        )

    @action(detail=True, methods=['get'], url_path='subscriptions')
    def list_subscription(self, request, pk=None):
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


class PortfolioViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.DestroyModelMixin,
):
    queryset = Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer

    permission_action_classes = {
        'list': (IsAdministrator,),
        'retrieve': (IsAdministrator | IsOwner,),
        'update': (IsAdministrator,),
        'partial_update': (IsAdministrator,),
        'destroy': (IsAdministrator | IsOwner,),
        'create': (IsAdministrator | IsUser,),
        'my_portfolios': (IsUser,),
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (IsUser,)
            )
        ]

    @action(detail=False, methods=['get'], url_path='my')
    def my_portfolios(self, request):
        return Response(
            portfolio_service.PortfolioService().find_my(request.user)
        )
