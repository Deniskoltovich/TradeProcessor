from rest_framework import serializers

from accounts.serializers.portfolio_serializers import (
    UserViewPortfolioSerializer,
)
from assets.models import Asset
from assets.serializers import AssetSerializer
from orders.models import AutoOrder, Order

# mypy: ignore-errors


class AdminViewOrderSerializer(serializers.ModelSerializer):
    portfolio = UserViewPortfolioSerializer(many=False, read_only=True)
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


class UserViewOrderSerializer(serializers.ModelSerializer):
    portfolio = UserViewPortfolioSerializer(many=False, read_only=True)
    asset = AssetSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            "portfolio",
            "asset",
            "initializer",
            "operation_type",
            "price",
            "quantity",
            "status",
        ]


class UpdateCreateOrderSerializer(serializers.ModelSerializer):
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


class AdminViewAutoOrderSerializer(serializers.ModelSerializer):
    portfolio = UserViewPortfolioSerializer(many=False, read_only=True)
    asset = AssetSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            "portfolio",
            "asset",
            "operation_type",
            "desired_price",
            "price_direction",
            "quantity",
            "status",
        ]


class UserViewAutoOrderSerializer(serializers.ModelSerializer):
    portfolio = UserViewPortfolioSerializer(many=False, read_only=True)
    asset = AssetSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            "portfolio",
            "asset",
            "operation_type",
            "desired_price",
            "price_direction",
            "quantity",
            "status",
        ]
