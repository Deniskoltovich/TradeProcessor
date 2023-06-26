from accounts.models import Portfolio, PortfolioAsset
from accounts.serializers import PortfolioSerializer
from assets.models import Asset
from assets.serializers import AssetSerializer
from orders.models import AutoOrder, Order
from rest_framework import serializers

# mypy: ignore-errors


class ListRetrieveOrderSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer(many=False, read_only=True)
    asset = AssetSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            "portfolio",
            "asset",
            "initializer",
            "operation_type",
            "price",
            "quantity",
            "status",
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "portfolio",
            "asset",
            "initializer",
            "operation_type",
            "price",
            "quantity",
        ]


class AutoOrderSerializer(serializers.ModelSerializer):
    portfolio_id = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )
    asset = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Order
        fields = [
            "portfolio_id",
            "asset",
            "operation_type",
            "desired_price" "price_direction",
            "quantity",
            "status",
        ]
