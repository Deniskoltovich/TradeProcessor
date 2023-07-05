import pytest
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from accounts.models import Portfolio, User
from assets.models import Asset
from orders.models import Order


@pytest.mark.django_db
class TestOrder:
    #  Tests that a new order can be created with valid data
    def test_create_order_valid_data(self, portfolio, asset):

        order = Order.objects.create(
            portfolio=portfolio,
            asset=asset,
            operation_type=Order.OperationType.BUY,
            price=10,
            quantity=1,
        )
        assert order.id is not None

    #  Tests that an existing order can be updated with valid data
    def test_update_order_valid_data(self, portfolio, asset):

        order = Order.objects.create(
            portfolio=portfolio,
            asset=asset,
            operation_type=Order.OperationType.BUY,
            price=10,
            quantity=1,
        )
        order.price = 20
        order.save()
        assert Order.objects.get(id=order.id).price == 20

    #  Tests that an existing order can be deleted
    def test_delete_order(self, portfolio, asset):

        order = Order.objects.create(
            portfolio=portfolio,
            asset=asset,
            operation_type=Order.OperationType.BUY,
            price=10,
            quantity=1,
        )
        order_id = order.id
        order.delete()
        with pytest.raises(Order.DoesNotExist):
            Order.objects.get(id=order_id)

    #  Tests that a new order cannot be created with invalid data
    def test_create_order_invalid_data(self, portfolio, asset):

        with pytest.raises(IntegrityError):
            Order.objects.create(
                portfolio=portfolio,
                asset=asset,
                operation_type=None,
                price=10,
                quantity=1,
            )

    #  Tests that a new order cannot be created with a negative price
    def test_create_order_negative_price(self, portfolio, asset):

        with pytest.raises(IntegrityError):
            Order.objects.create(
                portfolio=portfolio,
                asset=asset,
                operation_type=Order.OperationType.BUY,
                price=-10,
                quantity=1,
            )

    #  Tests that a new order cannot be created with a negative quantity
    def test_create_order_negative_quantity(self, portfolio, asset):

        with pytest.raises(IntegrityError):
            Order.objects.create(
                portfolio=portfolio,
                asset=asset,
                operation_type=Order.OperationType.BUY,
                price=10,
                quantity=-1,
            )
