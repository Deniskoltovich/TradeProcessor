import jwt
from accounts import serializers
from accounts.models import Portfolio, User
from accounts.permissions import IsAdministrator, IsOwner, IsUser
from accounts.services.auth_service import AuthService
from accounts.services.create_user_service import CreateUserService
from accounts.services.subscription_service import SubscriptionService
from accounts.services.update_user_service import UpdateUserService
from config import settings
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from rest_framework import generics, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class UserViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    GetSerializerClassMixin,
):
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
            return Response(UpdateUserService().execute(user, request.data))

    def create(self, request, *args, **kwargs):
        return Response(CreateUserService().execute(request), status=201)

    @permission_classes([IsUser])
    @action(
        detail=False,
        methods=['get'],
        url_path='refresh_token',
    )
    def refresh_token(self, request):
        return Response(AuthService().refresh(request))

    @permission_classes([AllowAny])
    @action(
        detail=False,
        methods=['post'],
        url_path='login',
    )
    def login(self, request):
        data = AuthService().login(request)
        response = Response()
        response.set_cookie(
            key='refreshtoken', value=data.get('refresh_token'), httponly=True
        )
        response.data = {
            'access_token': data.get('access_token'),
            'user': data.get('serialized_user'),
        }
        return response

    @permission_classes([IsOwner])
    @action(
        detail=True,
        methods=['post'],
        url_path='subscriptions/(?P<asset_id>[^/.]+)',
    )
    def add_subscription(self, request, pk, asset_id):
        return Response(SubscriptionService().add(request.user, asset_id))

    @permission_classes([IsOwner])
    @action(detail=True, methods=['get'], url_path='subscriptions')
    def list_subscription(self, request, pk):
        return Response(SubscriptionService().list(request.user))

    @permission_classes([IsOwner])
    @action(
        detail=True,
        methods=['DELETE'],
        url_path='subscriptions/(?P<asset_id>[^/.]+)/delete',
    )
    def delete_subscription(self, request, pk, asset_id):
        return Response(SubscriptionService().delete(request.user, asset_id))


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

    def get_permissions(self):
        permission_classes = []
        if self.action in ("list", "update", "partial_update"):
            permission_classes = [IsAdministrator]
        elif self.action in (
            "destroy",
            "retrieve",
        ):
            permission_classes = [IsAdministrator | IsOwner]
        elif self.action == 'create':
            permission_classes = [IsAdministrator | IsUser]

        return [permission() for permission in permission_classes]
