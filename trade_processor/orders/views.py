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
    permission_action_classes = {
        'list': (IsAdministrator | IsAnalyst,),
        'retrieve': (IsAdministrator | IsAnalyst | IsOwner,),
        'update': (IsAdministrator,),
        'partial_update': (IsAdministrator,),
        'destroy': (IsAdministrator,),
        'create': (IsUser | IsAdministrator,),
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (IsUser,)
            )
        ]

    def create(self, request, *args, **kwargs):
        try:
            return Response(OrderCreateService().execute(request.data))
        except ValidationError:
            return Response("Invalid data", status=405)
