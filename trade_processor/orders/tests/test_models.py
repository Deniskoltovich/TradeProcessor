# from accounts.models import Portfolio, User
# from assets.models import Asset
# from django.db.utils import DataError, IntegrityError
# from django.test import TestCase
# from orders.models import AutoOrder, Order
#
#
# class TestOrderModels(TestCase):
#     def setUp(self) -> None:
#         self.user = User.objects.create(
#             username='some_name', email='post@d.com'
#         )
#         self.portfolio = Portfolio.objects.create(
#             user=self.user,
#             name='some name',
#         )
#         self.asset = Asset.objects.create(
#             name='Bitcoin', type=Asset.Type.CRYPTOCURRENCY
#         )
#         return super().setUp()
#
#     def test_order_assigning_default_values(self):
#         order = Order.objects.create(
#             portfolio=self.portfolio,
#             asset=self.asset,
#             operation_type=Order.OperationType.BUY,
#             price=20000.00,
#             quantity=1,
#             status=Order.Status.FINISHED,
#         )
#         assert order.initializer == order.Initializer.MANUAL
#
#     def test_order_price_overflow(self):
#         with self.assertRaises(DataError):
#             Order.objects.create(
#                 portfolio=self.portfolio,
#                 asset=self.asset,
#                 operation_type=Order.OperationType.BUY,
#                 price=1000000000.00,
#                 quantity=1,
#                 status=Order.Status.FINISHED,
#             )
#
#     def test_auto_order_price_overflow(self):
#         with self.assertRaises(DataError):
#             AutoOrder.objects.create(
#                 portfolio=self.portfolio,
#                 asset=self.asset,
#                 operation_type=AutoOrder.OperationType.BUY,
#                 desired_price=1000000000.00,
#                 price_direction=AutoOrder.PriceDirection.LOWER,
#                 quantity=1,
#                 status=AutoOrder.Status.OPENED,
#             )
#
#     def test_required_operation_type_in_order(self):
#         with self.assertRaises(IntegrityError):
#             Order.objects.create(
#                 portfolio=self.portfolio,
#                 asset=self.asset,
#                 price=100000.00,
#                 quantity=1,
#                 status=Order.Status.FINISHED,
#             )
#
#     def test_required_price_direction_in_auto_order(self):
#         with self.assertRaises(IntegrityError):
#             AutoOrder.objects.create(
#                 portfolio=self.portfolio,
#                 asset=self.asset,
#                 operation_type=AutoOrder.OperationType.BUY,
#                 desired_price=1000.00,
#                 quantity=1,
#                 status=AutoOrder.Status.OPENED,
#             )
#
#     def test_required_operation_type_in_auto_order(self):
#         with self.assertRaises(IntegrityError):
#             AutoOrder.objects.create(
#                 portfolio=self.portfolio,
#                 asset=self.asset,
#                 operation_type=AutoOrder.OperationType.BUY,
#                 desired_price=10000.00,
#                 quantity=1,
#                 status=AutoOrder.Status.OPENED,
#             )
