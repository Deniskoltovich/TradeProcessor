from rest_framework import serializers

from accounts.models import Portfolio

# mypy: ignore-errors


class ListPortfolioSerializer(serializers.ModelSerializer):
    assets = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Portfolio
        fields = (
            'id',
            'user',
            "name",
            "description",
            "assets",
            "created_at",
            "updated_at",
        )


class CreatePortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            'user',
            "name",
            "description",
        )


class UpdatePortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = (
            "name",
            "description",
        )
