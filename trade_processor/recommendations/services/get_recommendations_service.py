from recommendations.models import Recommendation


class GetRecommendationService:
    @staticmethod
    def get_recommendation(user):
        recs = Recommendation.objects.filter(user=user)
        return recs
