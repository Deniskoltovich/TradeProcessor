from django.db import transaction

from orders.models import AutoOrder, Order
from orders.serializers import UpdateCreateOrderSerializer
from orders.services.create_order import OrderCreateService


class AutoOrderFinisher:
    @staticmethod
    @transaction.atomic()
    def check_opened_orders(asset):
        opened_orders = AutoOrder.objects.filter(
            asset=asset, status=AutoOrder.Status.OPENED
        )
        for order in opened_orders:

            if (
                (order.price_direction == AutoOrder.PriceDirection.LOWER
                and order.desired_price <= asset.current_price) or (
                order.order.price_direction == AutoOrder.PriceDirection.HIGHER
                and order.desired_price >= asset.current_price
            )
            ):
                AutoOrderFinisher._create_order(order)


    @staticmethod
    def _create_order(auto_order):
        data = {
            'price': auto_order.desired_price,
            "quantity": auto_order.quantity,
            'asset': auto_order.asset,
            "portfolio": auto_order.portfolio,
            "initializer": Order.Initializer.AUTO,
        }
        serializer = UpdateCreateOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        OrderCreateService.process_transaction(serializer.validated_data, auto_order=True)

