import pytest

from accounts.models import User
from assets.views import AssetViewSet


@pytest.mark.django_db
class TestAssetViewSet:
    #  Tests that a user with USER role can retrieve a list of assets
    def test_list_assets_as_user(self, mocker, user):
        # Arrange
        request = mocker.Mock()
        view = AssetViewSet()
        view.format_kwarg = None
        view.action = 'list'
        view.request = request
        request.user = user
        view.kwargs = {}
        # Act
        response = view.list(request)
        # Assert
        assert response.status_code == 200

    #  Tests that a user with ANALYST role can retrieve a list of assets
    def test_list_assets_as_analyst(self, mocker):
        # Arrange
        request = mocker.Mock()
        view = AssetViewSet()
        view.action = 'list'
        view.format_kwarg = None

        view.request = request
        view.kwargs = {}
        request.user.role = User.Role.ANALYST
        # Act
        response = view.list(request)
        # Assert
        assert response.status_code == 200

    #  Tests that a user with ADMIN role can retrieve a list of assets
    def test_list_assets_as_admin(self, mocker):
        # Arrange
        request = mocker.Mock()
        view = AssetViewSet()

        view.action = 'list'
        view.format_kwarg = None

        view.request = request
        view.kwargs = {}
        request.user.role = User.Role.ADMIN
        # Act
        response = view.list(request)
        # Assert
        assert response.status_code == 200

    #  Tests that a user with USER role can retrieve a single asset
    def test_retrieve_single_asset_as_user(self, mocker, asset, user):
        # Arrange
        request = mocker.Mock()
        request.user = user
        view = AssetViewSet()
        view.action = 'retrieve'
        view.request = request
        view.format_kwarg = None

        view.kwargs = {'pk': asset.pk}
        # Act
        response = view.retrieve(request, pk=asset.pk)
        # Assert
        assert response.status_code == 200

    #  Tests that a user with ANALYST role can retrieve a single asset
    def test_retrieve_single_asset_as_analyst(self, mocker, asset):
        # Arrange
        request = mocker.Mock()
        view = AssetViewSet()
        view.action = 'retrieve'
        view.request = request
        view.kwargs = {'pk': asset.pk}
        view.format_kwarg = None

        request.user.role = User.Role.ANALYST
        # Act
        response = view.retrieve(request, pk=asset.pk)
        # Assert
        assert response.status_code == 200

    #  Tests that a user with ADMIN role can retrieve a single asset
    def test_retrieve_single_asset_as_admin(self, mocker, asset):
        # Arrange
        request = mocker.Mock()
        view = AssetViewSet()
        view.action = 'retrieve'
        view.request = request
        view.format_kwarg = None

        view.kwargs = {'pk': asset.pk}
        request.user.role = User.Role.ADMIN
        # Act
        response = view.retrieve(request, pk=asset.pk)
        # Assert
        assert response.status_code == 200
