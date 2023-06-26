import django.db
from accounts.models import Portfolio, PortfolioAsset
from assets.models import Asset
from django.db import transaction
from orders.models import Order
from orders.serializers import CreateOrderSerializer


class OrderCreateService:
    @staticmethod
    @transaction.atomic()
    def execute(user, data):
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
