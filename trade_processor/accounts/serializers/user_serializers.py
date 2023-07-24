from rest_framework import serializers

from accounts.models import User

# mypy: ignore-errors


class AdminViewUserSerializer(serializers.ModelSerializer):

    portfolios = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            'username',
            "email",
            "avatar_url",
            "subscriptions",
            "balance",
            "portfolios",
            "status",
            "created_at",
            "updated_at",
        )


class UserViewUserSerializer(serializers.ModelSerializer):

    portfolios = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    subscriptions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )

    class Meta:
        model = User
        fields = (
            'username',
            "email",
            "subscriptions",
            "balance",
            "portfolios",
            "created_at",
            "updated_at",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            "email",
            "avatar_url",
            'password',
            "created_at",
            "updated_at",
        )


class UpdateUserByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("balance", 'status', 'role')


class PasswordUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs
