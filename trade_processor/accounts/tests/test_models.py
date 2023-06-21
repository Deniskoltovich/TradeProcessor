import mock
from accounts.models import Asset, CustomUser, Portfolio
from django.db.utils import IntegrityError
from django.test import TestCase


class TestAccountsModels(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.user = CustomUser.objects.get(username='admin')
        self.portfolio = Portfolio.objects.create(
            user=self.user,
            name='some name',
        )
        return super().setUp()

    def test_user_assigning_default_values(self):
        user = CustomUser.objects.create(
            username='some_name', email='post@d.com'
        )
        assert user.balance == 0.00
        assert user.avatar_url is None
        assert user.status == user.Status.DEACTIVE

    def test_unique_user_email(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(username='user', email='k@k.com')

    def test_unique_user_username(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(username='admin', email='post@d.com')
