from accounts.models import Portfolio
from accounts.serializers import PortfolioSerializer


class PortfolioService:
    @staticmethod
    def find_my(user):
        portfolios = Portfolio.objects.filter(user=user)
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data
