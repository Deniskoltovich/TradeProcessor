from recommendations.models import Recommendation
from recommendations.serializers import ListRecommendationSerializer


class GetRecommendationService:
    @staticmethod
    def get_recommendation(user):
        recs = Recommendation.objects.filter(user=user)
        return recs
