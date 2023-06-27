import django.db
from django.db import transaction

from accounts.models import Portfolio, PortfolioAsset
from assets.models import Asset
from orders.models import Order
from orders.serializers import CreateOrderSerializer


class OrderCreateService:
    @staticmethod
    @transaction.atomic()
    def execute(user, data):

        """
        The execute function is the main function of this service.
        It takes in a user and data, which are both required to create
         an order.
        The portfolio is created if it doesn't exist yet, and then the
         asset price is set to its current value.
        The serializer validates that all fields are correct, checks
         that there's enough balance for the purchase,
        and creates or updates a PortfolioAsset object with the new
         quantity of assets owned by this portfolio.
        Finally it saves everything into database.

        :param user: Get the user that is logged in
        :param data: Pass the data from the request to the execute
            function
        :return: The order data
        """
        portfolio, _ = Portfolio.objects.get_or_create(
            pk=data.get('portfolio'), user=user
        )
        data['portfolio'] = portfolio.id

        asset = Asset.objects.get(id=data.get('asset'))
        data['price'] = asset.current_price

        serializer = CreateOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        asset = serializer.validated_data.get('asset')
        OrderCreateService.check_conditions(
            serializer.validated_data, portfolio, asset
        )

        try:
            portfolio_asset = PortfolioAsset.objects.get(
                asset=asset, portfolio=portfolio
            )
            portfolio_asset.quantity += serializer.validated_data['quantity']
        except PortfolioAsset.DoesNotExist:
            PortfolioAsset.objects.create(
                asset=asset,
                portfolio=portfolio,
                quantity=serializer.validated_data['quantity'],
            )
        user.balance -= (
            asset.current_price * serializer.validated_data['quantity']
        )
        user.save()
        serializer.save()
        return serializer.data

    @staticmethod
    def check_conditions(validated_data, portfolio, asset):

        """
        The check_conditions function checks if the user has enough
         balance to buy or sell an asset.
        It also checks if the user is trying to sell an asset that he
         doesn't have in his portfolio.

        :param validated_data: Get the data from the serializer
        :param portfolio: To check if the user has enough balance to buy
            an asset
        :param asset: Get the asset object from the database
        :return: An error if the user doesn't have enough balance to buy
         or sell an asset
        """
        if validated_data["operation_type"] == Order.OperationType.SELL:
            try:
                PortfolioAsset.objects.get(asset=asset, portfolio=portfolio)
            except PortfolioAsset.DoesNotExist:
                raise django.db.IntegrityError(
                    "You don't have this asset in your portfolios"
                )
        if (
            validated_data["operation_type"] == Order.OperationType.SELL
            and validated_data['quantity']
            > PortfolioAsset.objects.get(
                asset=asset, portfolio=portfolio
            ).quantity
        ):
            raise django.db.IntegrityError(
                "You don't have enough assets to sell"
            )
        elif (
            validated_data["operation_type"] == Order.OperationType.BUY
            and validated_data['price'] * validated_data['quantity']
            > portfolio.user.balance
        ):
            raise django.db.IntegrityError(
                "Not enough balance for this operation"
            )
