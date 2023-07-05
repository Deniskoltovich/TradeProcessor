# import decimal
# import os
#
# from accounts.models import User
# from assets.models import Asset
# from django.test import Client, RequestFactory, TestCase
# from orders.views import OrderViewSet
#
#
# class TestUserView(TestCase):
#     fixtures = ['users.json']
#
#     def setUp(self) -> None:
#         self.client = Client()
#         self.asset = Asset.objects.create(
#             name='Bit', type=Asset.Type.CRYPTOCURRENCY
#         )
#         self.user = User.objects.get(username='user')
#         self.url = (
#             f"http://{os.environ.get('APP_HOST'):{os.environ.get('APP_PORT')}}"
#         )
#         return super().setUp()
#
#     def test_is_admin_permission_for_orders_list(self):
#         request = RequestFactory().get(f'{self.url}/orders/')
#
#         request.user = User.objects.get(username='admin')
#         response = OrderViewSet.as_view({'get': 'list'})(request)
#
#         self.assertEquals(response.status_code, 200)
#
#     def test_is_user_permission_for_order_list(self):
#         request = RequestFactory().get(f'{self.url}/orders/')
#
#         request.user = User.objects.get(username='user')
#         response = OrderViewSet.as_view({'get': 'list'})(request)
#
#         self.assertEquals(response.status_code, 403)
