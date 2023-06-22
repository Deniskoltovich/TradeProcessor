from accounts.permissions import IsAdministrator, IsAnalyst, IsOwner, IsUser
from assets.models import Asset
from assets.serializers import AssetSerializer
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from rest_framework import generics, viewsets


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

    def get_permissions(self):
        permission_classes = []
        if self.action in (
            "destroy",
            "update",
            "partial_update",
            'create',
        ):
            permission_classes = [IsAdministrator]
        else:
            permission_classes = [IsAdministrator | IsAnalyst | IsUser]

        return [permission() for permission in permission_classes]
