import os

from accounts.models import User
from django.test import Client, TestCase


class TestUserView(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.url = (
            f"http://{os.environ.get('APP_HOST'):{os.environ.get('APP_PORT')}}"
        )
        return super().setUp()

    def test_admin_get_accounts_list(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get(f'{self.url}/accounts/')

        self.assertEquals(response.status_code, 200)

    def test_user_get_accounts_list(self):
        self.client.login(username='user', password='user')

        response = self.client.get(f'{self.url}/accounts/')

        self.assertEquals(response.status_code, 403)

    def test_user_creation(self):
        data = {
            'username': 'user1',
            'email': 'user@g.com',
            'password': 'user1234',
        }

        response = self.client.post(f'{self.url}/accounts/', data)

        self.assertEquals(response.status_code, 201)
