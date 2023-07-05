import pytest
import rest_framework

from accounts.models import Portfolio, User
from accounts.views.portfolio_views import PortfolioViewSet


@pytest.mark.django_db
class TestPortfolioViewSet:
    #  Tests that the list method returns a list of all portfolios for an admin user
    def test_list_method_returns_all_portfolios_for_admin_user(
        self, mocker, portfolio
    ):

        request = mocker.Mock(user=mocker.Mock(role=User.Role.ADMIN))
        view = PortfolioViewSet()
        view.get_object = mocker.Mock(return_value=request.user)
        view.request = mocker.Mock(return_value=request)
        view.action = 'list'
        view.format_kwarg = mocker.Mock(return_value={})
        view.request = request
        response = view.list(request)
        assert response.status_code == 200
        assert len(response.data) == Portfolio.objects.count()

    def test_retrieve_method_raises_permission_denied_for_non_admin_owner(
        self, mocker, portfolio
    ):
        request = mocker.Mock(user=mocker.Mock(role=User.Role.USER))
        view = PortfolioViewSet()
        view.request = request
        view.action = 'retrieve'
        view.kwargs = {'pk': portfolio.pk}
        view.format_kwarg = None

        with pytest.raises(rest_framework.exceptions.PermissionDenied):
            view.retrieve(request, pk=portfolio.pk)

    def test_update_method_returns_404_error_for_non_owner_user(
        self, mocker, portfolio
    ):
        portfolio = Portfolio.objects.first()
        request = mocker.Mock(user=mocker.Mock(role=User.Role.USER))
        view = PortfolioViewSet()
        view.request = request
        view.action = 'update'
        view.kwargs = {'pk': portfolio.pk, 'name': 'New Name'}
        view.format_kwarg = None

        with pytest.raises(rest_framework.exceptions.PermissionDenied):
            view.update(request)
