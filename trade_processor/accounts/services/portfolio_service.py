from accounts.models import Portfolio
from accounts.serializers import PortfolioSerializer


class PortfolioService:
    @staticmethod
    def find_my(user):
        """
        The find_my function returns a list of all portfolios belonging
         to the user.
        Args:
             user (User): The User object that is currently logged in.

        :param user: Filter the portfolio table to only return
            portfolios that belong to the user
        :return: A list of dictionaries with portfolio data
        """
        portfolios = Portfolio.objects.filter(user=user)
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data
