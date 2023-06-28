from accounts.models import Portfolio


class PortfolioService:
    @staticmethod
    def get_portfolio_by_user(user):
        """
        The get_portfolio_by_user function returns a list of all
         portfolios belonging
         to the user.
        Args:
             user (User): The User object that is currently logged in.

        """
        return Portfolio.objects.filter(user=user)
