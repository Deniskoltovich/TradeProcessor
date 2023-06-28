from recommendations.models import Recommendation
from recommendations.serializers import ListRecommendationSerializer


class GetRecommendationService:
    @staticmethod
    def execute(user):
        recs = Recommendation.objects.filter(user=user)
        data = ListRecommendationSerializer(recs, many=True).data
        return data
