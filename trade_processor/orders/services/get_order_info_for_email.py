from accounts.models import Portfolio
from assets.models import Asset


class GetOrderInfoService:
    @staticmethod
    def get_info(order_data, errors=None, auto=False):

        """
        The get_info function takes an order_data dictionary and a
         list of errors. If there are no errors, it returns a message
         with the asset name, current price, quantity and operation
         type. If there are errors in the list of error messages
         passed to it, it returns a message with the asset name and
         current price along with all error messages.

        :param order_data: Pass the data of the order to be processed
        :param errors: Pass the errors to the function
        :return: A tuple of two values:
        """
        asset = Asset.objects.get(pk=order_data['asset'])
        price = (
            asset.current_price if not auto else order_data["desired_price"]
        )
        if errors:
            message = (
                f'Your order on {asset}, price: '
                f'{price} was declined:\n' + ' '.join(errors)
            )
        else:
            message = (
                f'Your order on {asset} is {order_data["status"].lower()}'
                ' successfully:'
                f'\n price: {price}\n'
                f' quantity: {order_data["quantity"]}\n'
                f' operation:{order_data["operation_type"]}'
                f'price direction: {order_data["price_direction"]}'
                if auto
                else ''
            )
        return message, Portfolio.objects.get(pk=order_data['portfolio'])
