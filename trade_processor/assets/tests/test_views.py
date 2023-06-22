import os

from accounts.models import User
from assets.models import Asset
from assets.views import AssetViewSet
from django.test import Client, RequestFactory, TestCase


class TestUserView(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.asset = Asset.objects.create(
            name='Bit', type=Asset.Type.CRYPTOCURRENCY
        )
        self.url = (
            f"http://{os.environ.get('APP_HOST'):{os.environ.get('APP_PORT')}}"
        )
        return super().setUp()

    def test_is_admin_permission_for_get_assets_list(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get(f'{self.url}/assets/')

        self.assertEquals(response.status_code, 200)

    def test_is_user_permission_for_get_assets_list(self):
        request = RequestFactory().get(f'{self.url}/assets/')

        request.user = User.objects.get(username='user')
        response = AssetViewSet.as_view({'get': 'list'})(request)
        self.assertEquals(response.status_code, 200)

    def test_asset_creation_by_admin(self):
        self.client.login(username='admin', password='admin')
        data = {
            'name': 'Bitcoin',
            'type': Asset.Type.CRYPTOCURRENCY,
        }
        response = self.client.post(f'{self.url}/assets/', data)
        self.assertEquals(response.status_code, 201)

    def test_asset_creation_by_user(self):
        self.client.login(username='user', password='user')
        data = {
            'name': 'Bitcoin',
            'type': Asset.Type.CRYPTOCURRENCY,
        }
        response = self.client.post(f'{self.url}/assets/', data)
        self.assertEquals(response.status_code, 403)
