import os

from accounts.models import Portfolio, User
from assets.models import Asset
from django.test import Client, TestCase


class TestPortfolioView(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='user')
        self.asset = Asset.objects.create(
            name='Bitcoin', type=Asset.Type.CRYPTOCURRENCY
        )
        self.url = (
            f"http://{os.environ.get('APP_HOST'):{os.environ.get('APP_PORT')}}"
        )
        return super().setUp()

    def test_is_admin_permission_for_get_portfolios_list(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get(f'{self.url}/accounts/portfolios/')

        self.assertEquals(response.status_code, 200)

    def test_user_get_portfolios_list(self):
        self.client.login(username='user', password='user')

        response = self.client.get(f'{self.url}/accounts/portfolios/')

        self.assertEquals(response.status_code, 403)

    def test_is_user_permission_for_portfolio_creation(self):
        self.client.login(username='user', password='user')
        data = {
            'user': self.user,
        }

        response = self.client.post(f'{self.url}/accounts/portfolios/', data)

        self.assertEquals(response.status_code, 403)

    def test_is_admin_permission_for_delete(self):
        self.client.login(username='admin', password='admin')
        portfolio = Portfolio.objects.create(user=self.user)
        response = self.client.delete(
            f'{self.url}/accounts/portfolios/{portfolio.id}/'
        )

        self.assertEquals(response.status_code, 204)

    def test_is_admin_permission_for_retrieve(self):
        self.client.login(username='admin', password='admin')
        portfolio = Portfolio.objects.create(user=self.user)
        portfolio.assets.add(self.asset)
        portfolio.save()

        response = self.client.get(
            f'{self.url}/accounts/portfolios/{portfolio.id}/'
        )

        self.assertEquals(response.status_code, 200)
