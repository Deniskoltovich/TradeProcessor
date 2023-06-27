from rest_framework import serializers

from accounts.models import Portfolio

# mypy: ignore-errors


class PortfolioSerializer(serializers.ModelSerializer):
    assets = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Portfolio
        fields = [
            'id',
            'user',
            "name",
            "description",
            "assets",
            "created_at",
            "updated_at",
        ]
