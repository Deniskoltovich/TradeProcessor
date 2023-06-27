from accounts.models import User
from orders import serializers
from orders.models import AutoOrder, Order


class ListTransactions:
    @staticmethod
    def execute(user_id):
        """
        The execute function takes a user_id as an argument and returns
         a dictionary containing all orders and auto-orders for that
          user.


        :param user_id: Get the user object from the database
        :return: A dictionary with two keys: orders and auto_orders
        """
        user = User.objects.get(pk=user_id)
        order_transactions = Order.objects.filter(
            portfolio__user=user, status=Order.Status.FINISHED
        )
        auto_order_transactions = AutoOrder.objects.filter(
            portfolio__user=user, status=AutoOrder.Status.FINISHED
        )
        orders_data = serializers.ListRetrieveOrderSerializer(
            order_transactions, many=True
        ).data
        auto_orders_data = serializers.ListAutoOrderSerializer(
            auto_order_transactions, many=True
        ).data
        return {'orders': orders_data, 'auto_orders': auto_orders_data}
