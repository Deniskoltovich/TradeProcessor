import django.db
from django.db import transaction
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import (
    IsAdministrator,
    IsAnalyst,
    IsOwner,
    IsUser,
)
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from orders import serializers
from orders.models import AutoOrder, Order
from orders.serializers import UpdateCreateOrderSerializer
from orders.services.create_order import OrderCreateService
from orders.tasks.order_creation_email import send_email_with_order_info


class OrderViewSet(
    GetSerializerClassMixin,
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.DestroyModelMixin,
):
    queryset = Order.objects.all()
    serializer_class = serializers.UserViewOrderSerializer

    serializer_role_action_classes = {
        (User.Role.ADMIN, 'list'): serializers.AdminViewOrderSerializer,
        (User.Role.ADMIN, 'retrieve'): serializers.AdminViewOrderSerializer,
    }

    serializer_action_classes = {
        'create': serializers.UpdateCreateOrderSerializer,
        'update': serializers.UpdateCreateOrderSerializer,
        'partial_update': serializers.UpdateCreateOrderSerializer,
    }

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

    @transaction.atomic()
    def create(self, request, *args, **kwargs):

        try:
            order_data = OrderCreateService.create(request.user, request.data)
            serializer = UpdateCreateOrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            OrderCreateService.process_transaction(serializer.validated_data)
            send_email_with_order_info.delay(serializer.data)
            return Response(serializer.data)
        except ValidationError:
            return Response("Invalid data", status=400)
        except django.db.IntegrityError as e:
            order.status = Order.Status.CANCELLED
            order.save()
            send_email_with_order_info.delay(
                UpdateCreateOrderSerializer(order).data, e.args
            )
            return Response(e.args, exception=True)


class AutoOrderViewSet(
    GetSerializerClassMixin,
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.DestroyModelMixin,
):
    queryset = AutoOrder.objects.all()
    serializer_class = serializers.UserViewAutoOrderSerializer

    serializer_role_action_classes = {
        (User.Role.ADMIN, 'list'): serializers.AdminViewAutoOrderSerializer,
        (
            User.Role.ADMIN,
            'retrieve',
        ): serializers.AdminViewAutoOrderSerializer,
    }

    serializer_action_classes = {
        'list': serializers.UserViewAutoOrderSerializer,
        'create': serializers.UpdateCreateAutoOrderSerializer,
        'update': serializers.UpdateCreateAutoOrderSerializer,
        'partial_update': serializers.UpdateCreateAutoOrderSerializer,
    }

    permission_action_classes = {
        'list': (IsAdministrator | IsAnalyst | IsOwner,),
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
            auto_order_data = OrderCreateService.create(
                request.user, request.data, auto_order=True
            )
            serializer = self.get_serializer_class()(data=auto_order_data)

            serializer.is_valid(raise_exception=True)
            auto_order = serializer.save()
            OrderCreateService.process_auto_order(serializer.validated_data)
            send_email_with_order_info.delay(serializer.data, auto=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(f"Invalid data: {e.args}", status=400)
        except django.db.IntegrityError as e:
            auto_order.status = Order.Status.CANCELLED
            auto_order.save()
            send_email_with_order_info.delay(
                UpdateCreateOrderSerializer(auto_order).data, e.args, auto=True
            )
            return Response(e.args, exception=True)

    def get_queryset(self):
        return AutoOrder.objects.filter(portfolio__user=self.request.user)
