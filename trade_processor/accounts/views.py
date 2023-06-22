from accounts import serializers
from accounts.models import Portfolio, User
from accounts.permissions import IsAdministrator, IsOwner
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from rest_framework import generics, viewsets


class UserViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.DestroyModelMixin,
    GetSerializerClassMixin,
):
    queryset = User.objects.all()
    serializer_class = serializers.ListUserSerializer

    serializer_action_classes = {
        "update": serializers.UpdateUserSerializer,
        "partial_update": serializers.UpdateUserSerializer,
    }

    def get_permissions(self):
        permission_classes = []
        if self.action in ("list", "destroy"):
            permission_classes = [IsAdministrator]
        elif self.action in ("retrieve", "update", "partial_update"):
            permission_classes = [IsAdministrator | IsOwner]

        return [permission() for permission in permission_classes]


class PortfolioViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.DestroyModelMixin,
    GetSerializerClassMixin,
):
    queryset = Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer

    serializer_action_classes = {
        "update": serializers.UpdateUserSerializer,
        "partial_update": serializers.UpdateUserSerializer,
    }

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdministrator]
        elif self.action in (
            "create",
            "destroy",
            "update",
            "partial_update",
            "retrieve",
        ):
            permission_classes = [IsAdministrator | IsOwner]

        return [permission() for permission in permission_classes]
