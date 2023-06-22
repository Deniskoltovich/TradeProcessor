from accounts.models import Portfolio
from orders.models import AutoOrder, Order
from rest_framework import serializers

# mypy: ignore-errors


class OrderSerializer(serializers.ModelSerializer):
    portfolio_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True
    )
    asset = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Order
        fields = [
            "portfolio_id",
            "asset",
            "initializer",
            "operation_type",
            "price",
            "quantity",
            "status",
        ]

    def validate(self, data):
        if data["operation_type"] == Order.OperationType.SELL:
            return data
        user_balance = Portfolio.objects.get(
            pk=data["portfolio_id"]
        ).user.balance
        if data["price"] * data["quantity"] > user_balance:
            raise serializers.ValidationError(
                "Not enough balance for this operation"
            )
        return data


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
