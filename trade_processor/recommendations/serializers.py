from rest_framework import serializers

from recommendations.models import Recommendation

# mypy: ignore-errors


class CreateRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = (
            'id',
            'asset',
            'user',
            'relevance_value',
        )


class ListRecommendationSerializer(serializers.ModelSerializer):
    asset = serializers.SlugRelatedField(
        read_only=True, many=False, slug_field='name'
    )

    class Meta:
        model = Recommendation
        fields = ('asset',)
