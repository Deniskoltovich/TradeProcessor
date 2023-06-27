from rest_framework import generics, viewsets

from accounts.permissions import (
    IsAdministrator,
    IsAnalyst,
    IsOwner,
    IsUser,
)
from assets.models import Asset
from assets.serializers import AssetSerializer
from mixins.get_serializer_class_mixin import GetSerializerClassMixin


class AssetViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.DestroyModelMixin,
):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    permission_action_classes = {
        'list': (IsAdministrator | IsAnalyst | IsUser,),
        'retrieve': (IsAdministrator | IsAnalyst | IsUser,),
        'update': (IsAdministrator,),
        'partial_update': (IsAdministrator,),
        'destroy': (IsAdministrator,),
    }

    def get_permissions(self):

        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (IsUser,)
            )
        ]
