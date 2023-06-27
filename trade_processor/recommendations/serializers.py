from rest_framework import serializers

from recommendations.models import Recommendation


class CreateRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class ListRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = [
            'user',
            'asset',
        ]
