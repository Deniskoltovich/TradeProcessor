import django.http
import pytest

from accounts.models import User
from orders.models import Order
from orders.views import OrderViewSet


@pytest.mark.django_db
class TestOrderViewSet:
    #  Tests that an admin can list orders
    def test_admin_list_orders(self, mocker, user):
        request = mocker.Mock()
        request.user = user

        view = OrderViewSet()
        view.action = 'list'
        view.kwargs = {}
        view.request = request

        view.format_kwarg = None
        response = view.list(request)
        assert response.status_code == 200

    #  Tests that an analyst can list orders
    def test_analyst_list_orders(self, mocker):
        request = mocker.Mock(user=mocker.Mock(role=User.Role.ANALYST))
        view = OrderViewSet()
        view.action = 'list'
        view.kwargs = {}
        view.request = request
        view.format_kwarg = None
        response = view.list(request)
        assert response.status_code == 200

    #  Tests that an admin can retrieve an order
    def test_admin_retrieve_order(self, mocker, asset, portfolio):
        order = Order.objects.create(
            asset=asset,
            portfolio=portfolio,
            operation_type=Order.OperationType.BUY,
            quantity=5,
            price=asset.current_price,
        )
        request = mocker.Mock(user=mocker.Mock(role=User.Role.ADMIN))
        view = OrderViewSet()
        view.action = 'retrieve'
        view.kwargs = {'pk': order.pk}
        view.format_kwarg = None
        view.request = request

        response = view.retrieve(request)
        assert response.status_code == 200

    #  Tests that a user can create an order
    def test_user_create_order(self, mocker, portfolio, asset):
        user = portfolio.user

        data = {
            'asset': asset.pk,
            'portfolio': portfolio.pk,
            'operation_type': Order.OperationType.BUY,
            'quantity': 5,
        }
        request = mocker.Mock(user=user, data=data)
        view = OrderViewSet()
        view.action = 'create'
        view.kwargs = data
        view.format_kwarg = None
        view.request = request

        response = view.create(request)

        assert response.status_code == 200

    def test_user_create_order_with_invalid_data(
        self, mocker, portfolio, asset
    ):
        user = portfolio.user

        data = {
            'asset': asset.pk,
            'portfolio': portfolio.pk,
            'operation_type': Order.OperationType.BUY,
            'quantity': -5,
        }
        request = mocker.Mock(user=user, data=data)
        view = OrderViewSet()
        view.action = 'create'
        view.kwargs = data
        view.format_kwarg = None
        view.request = request

        response = view.create(request)

        assert response.status_code == 400
