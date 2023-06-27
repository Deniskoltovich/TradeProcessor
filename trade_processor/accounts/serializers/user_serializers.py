from rest_framework import serializers

from accounts.models import User

# mypy: ignore-errors


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
