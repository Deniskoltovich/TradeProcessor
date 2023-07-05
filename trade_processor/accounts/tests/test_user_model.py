import pytest
from django.db import IntegrityError

from accounts.models import User
from assets.models import Asset


@pytest.mark.django_db
class TestUser:
    #  Tests that a user can be created with all required fields
    @pytest.mark.django_db
    def test_create_user(self):
        print(User.objects.all(), 'n\n\n\n\\nn\n\n\n\n\n\n')
        user = User.objects.create_user(
            email='test@test.com', password='password', username='test'
        )
        assert user.email == 'test@test.com'
        assert user.username == 'test'
        assert user.role == 'User'
        assert user.balance == 0.00
        assert user.status == 'Inactive'
        assert user.subscriptions.count() == 0

    #  Tests that a superuser can be created with all required fields
    @pytest.mark.django_db
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='test@test.com', password='password', username='test'
        )
        assert user.email == 'test@test.com'
        assert user.username == 'test'
        assert user.role == 'Admin'
        assert user.balance == 0.00
        assert user.status == 'Inactive'
        assert user.subscriptions.count() == 0
        assert user.is_superuser
        assert user.is_staff

    #  Tests that an error is raised when creating a user with a duplicate email
    @pytest.mark.django_db
    def test_create_user_duplicate_email(self):
        User.objects.create_user(
            email='test@test.com', password='password', username='test'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='test@test.com', password='password', username='test1'
            )

    @pytest.mark.django_db
    def test_create_user_duplicate_username(self):
        User.objects.create_user(
            email='test@test.com', password='password', username='test'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='test@test.com', password='password', username='test1'
            )

    #  Tests that an error is raised when creating a user without an email
    @pytest.mark.django_db
    def test_create_user_no_email(self):
        with pytest.raises(TypeError):
            User.objects.create_user(email=None, password='password')

    @pytest.mark.django_db
    #  Tests that an error is raised when creating a superuser without a password
    def test_create_superuser_no_password(self):
        with pytest.raises(TypeError):
            User.objects.create_superuser(email='test@test.com', password=None)

    @pytest.mark.django_db
    def test_add_subscription(self):
        user = User.objects.create_user(
            email='test@test.com', password='password'
        )
        user.subscriptions.add(
            Asset.objects.create(
                name='Nonexistent Asset',
                type=Asset.Type.SHARE,
                current_price=100.00,
            )
        )
        assert user.subscriptions.count() == 1
