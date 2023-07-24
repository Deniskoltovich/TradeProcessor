import pytest

from accounts.models import User
from accounts.serializers import user_serializers
from accounts.views.user_views import UserViewSet
from assets.models import Asset


@pytest.mark.django_db
class TestUserViewSet:
    #  Tests that a user can be retrieved successfully
    def test_retrieve_user_successfully(self, mocker):
        # Arrange
        user = User.objects.create_user(
            email='test1@test.com', password='password', username='test1'
        )
        request = mocker.Mock()
        kwargs = {'pk': user.pk}
        view = UserViewSet()
        view.get_object = mocker.Mock(return_value=user)
        view.request = mocker.Mock(return_value=request)
        view.format_kwarg = mocker.Mock(return_value=kwargs)
        view.get_serializer_class = mocker.Mock(
            return_value=user_serializers.UserViewUserSerializer
        )
        # Act
        response = view.retrieve(request, **kwargs)
        # Assert
        assert response.status_code == 200
        assert response.data['email'] == user.email
        assert response.data['balance'] == '0.00'

    #  Tests that a user can be created successfully
    def test_create_user_successfully(self, mocker):
        # Arrange
        request = mocker.Mock()
        request.data = {
            'email': 't1est@test.com',
            'username': 'username',
            'password': 'password',
        }
        view = UserViewSet()
        view.get_serializer_class = mocker.Mock(
            return_value=user_serializers.UserViewUserSerializer
        )
        # Act
        response = view.create(request)
        # Assert
        assert response.status_code == 201
        assert response.data['username'] == 'username'
        assert response.data['email'] == 't1est@test.com'

    #  Tests that a user can update their password successfully
    def test_update_password_successfully(self, mocker):
        # Arrange
        user = User.objects.create_user(
            email='test@test.com', password='password'
        )
        request = mocker.Mock()
        request.user = user
        request.data = {'password': 'new_password'}
        view = UserViewSet()
        view.get_object = mocker.Mock(return_value=user)
        # Act
        response = view.update(request, pk=user.pk)
        # Assert
        assert response.status_code == 200

    #  Tests that an admin can update a user's information successfully
    def test_admin_update_user_information_successfully(self, mocker):
        # Arrange
        admin = User.objects.create_superuser(
            email='admin@test.com', password='password', username='admin'
        )
        user = User.objects.create_user(
            email='test@test.com', password='password', username='user'
        )
        request = mocker.Mock()
        request.user = admin
        request.data = {'balance': 100.00}
        kwargs = {'pk': user.pk}
        view = UserViewSet()
        view.get_object = mocker.Mock(return_value=user)
        view.get_serializer_class = mocker.Mock(
            return_value=user_serializers.UpdateUserByAdminSerializer
        )
        # Act
        response = view.update(request, **kwargs)
        # Assert
        assert response.status_code == 200
        assert response.data['balance'] == str(user.balance + 100.00) + '0'

    #  Tests that a user can list their subscriptions successfully
    def test_list_user_subscriptions_successfully(self, mocker):
        # Arrange
        user = User.objects.create_user(
            email='test@test.com', password='password'
        )
        asset = Asset.objects.create(
            name='Test Asset',
            logo_url='http://test.com',
            description='Test Description',
            type='Test Type',
            current_price=100.00,
        )
        user.subscriptions.add(asset)
        request = mocker.Mock()
        request.user = user
        view = UserViewSet()
        # Act
        response = view.list_subscription(request, pk=user.pk)
        # Assert
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == asset.name
        assert response.data[0]['logo_url'] == asset.logo_url
        assert response.data[0]['description'] == asset.description
        assert response.data[0]['type'] == asset.type
        assert (
            response.data[0]['current_price'] == str(asset.current_price) + '0'
        )
