from rest_framework import serializers

from recommendations.models import Recommendation


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
    class Meta:
        model = Recommendation
        fields = (
            'user',
            'asset',
        )
