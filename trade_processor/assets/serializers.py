from rest_framework import serializers

from assets.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = (
            'id',
            'name',
            'logo_url',
            'description',
            'type',
            'current_price',
        )
