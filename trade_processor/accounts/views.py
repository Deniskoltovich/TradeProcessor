from accounts import serializers
from accounts.models import Portfolio, User
from accounts.permissions import IsAdministrator, IsOwner, IsUser
from accounts.services.subscription_service import SubscriptionService
from accounts.services.update_user_service import UpdateUserService
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from rest_framework import generics, viewsets
from rest_framework.decorators import action, permission_classes
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
    }

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdministrator]
        elif self.action in ('retrieve', "partial_update"):
            permission_classes = [IsAdministrator, IsOwner]

        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        if request.user.Role.ADMIN:
            return super().update(request, *args, **kwargs)
        else:
            user = self.get_object()
            print('\n\n\n\\nn\\n')
            return Response(UpdateUserService().execute(user, request.data))

    @permission_classes([IsOwner])
    @action(
        detail=True,
        methods=['post'],
        url_path='subscriptions/(?P<asset_id>[^/.]+)',
    )
    def add_subscription(self, requset, pk, asset_id):
        return Response(SubscriptionService().add(requset.user, asset_id))

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
    def delete_subscription(self, requset, pk, asset_id):
        return Response(SubscriptionService().delete(requset.user, asset_id))


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
