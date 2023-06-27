import django.db
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.permissions import (
    IsAdministrator,
    IsAnalyst,
    IsOwner,
    IsUser,
)
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from orders import serializers
from orders.models import Order
from orders.services.order_create_service import OrderCreateService


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
    serializer_class = serializers.ListRetrieveOrderSerializer
    serializer_action_classes = {
        'create': serializers.CreateOrderSerializer,
    }
    permission_action_classes = {
        'list': (IsAdministrator | IsAnalyst,),
        'retrieve': (IsAdministrator | IsAnalyst | IsOwner,),
        'update': (IsAdministrator,),
        'partial_update': (IsAdministrator,),
        'destroy': (IsAdministrator,),
        'create': (IsUser | IsAdministrator,),
        'list_transactions': (IsAdministrator, IsOwner, IsAnalyst),
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
            return Response(
                OrderCreateService().execute(request.user, request.data)
            )
        except ValidationError:
            return Response("Invalid data", status=405)
        except django.db.IntegrityError as e:
            return Response(e.args, exception=True)
