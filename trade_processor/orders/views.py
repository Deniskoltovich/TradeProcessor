from accounts.permissions import IsAdministrator, IsAnalyst, IsOwner, IsUser
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from orders.models import Order
from orders.serializers import ListRetrieveOrderSerializer
from orders.services.order_create_service import OrderCreateService
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class OrderViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.DestroyModelMixin,
    GetSerializerClassMixin,
):
    queryset = Order.objects.all()
    serializer_class = ListRetrieveOrderSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in (
            "destroy",
            "update",
            "partial_update",
        ):
            permission_classes = [IsAdministrator]
        elif self.action == 'create':
            permission_classes = [IsUser | IsAdministrator]
        elif self.action == 'list':
            permission_classes = [IsAdministrator | IsAnalyst]
        elif self.action == 'retrieve':
            permission_classes = [IsAdministrator | IsAnalyst | IsOwner]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            return Response(OrderCreateService().execute(request.data))
        except ValidationError:
            return Response("Invalid data", status=405)
