from accounts.models import Portfolio, User
from assets.serializers import AssetSerializer
from rest_framework import serializers

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


class ListUserSerializer(serializers.ModelSerializer):

    portfolios_id = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            'username',
            "email",
            "avatar_url",
            "subscriptions",
            "balance",
            "portfolios_id",
            "created_at",
            "updated_at",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            "email",
            "avatar_url",
            'password',
            "created_at",
            "updated_at",
        ]


class PartialUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "balance",
            'status',
        ]


class PasswordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class SubscriptionSerializer(serializers.Serializer):
    user = ListUserSerializer(many=False)
    asset = AssetSerializer(many=False)
