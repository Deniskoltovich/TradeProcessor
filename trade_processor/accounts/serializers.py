from accounts.models import Portfolio, User
from rest_framework import serializers

# mypy: ignore-errors


class PortfolioSerializer(serializers.ModelSerializer):
    assets = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Portfolio
        fields = ["name", "description", "assets", "created_at", "updated_at"]


class ListUserSerializer(serializers.ModelSerializer):

    portfolios_id = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "avatar_url",
            "subscriptions",
            "balance",
            "portfolios_id",
            "created_at",
            "updated_at",
        ]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "avatar_url",
            "subscriptions",
        ]
