import decimal

from django.db.models import F, Q
from django.db.models.functions import Abs

from assets.models import Asset
from recommendations.models import Recommendation
from recommendations.serializers import CreateRecommendationSerializer


class CreateRecommendationService:
    @staticmethod
    def execute(asset, user):

        """
        The execute function takes in a user and an asset, and returns
         the new recommendation for that user.
        It first deletes any existing recommendations for that
         asset/user pair.
        Then it checks if the number of recommendations is 5, which
         means we need to switch out one of them with a new one. If so,
         it calls switch_recommendation(). Otherwise, it gets all
         assets associated with this user, then creates a new
         recommendation

        :param asset: Get the asset that is being recommended
        :param user: Get the user's recommendations and assets
        :return: A serialized recommendation object
        """
        try:
            Recommendation.objects.get(user=user, asset=asset).delete()
        except Recommendation.DoesNotExist:
            pass

        user_recommendations = Recommendation.objects.filter(user=user)
        if user_recommendations.count() == 5:
            return CreateRecommendationService.switch_recommendation(user)

        user_assets = CreateRecommendationService.get_user_assets(user)
        recommendation = CreateRecommendationService.create_new_recommendation(
            user, user_assets
        )
        serializer = CreateRecommendationSerializer(instance=recommendation)
        return serializer.data

    @staticmethod
    def switch_recommendation(user):

        """
        It deletes the current recommendation and creates a new one,
         based on the user's assets.

        :param user: Get the user's assets and create a new
            recommendation for them
        :return: A new recommendation for the user
        """
        less_relevance_recommendation = Recommendation.objects.latest()
        less_relevance_recommendation.delete()
        user_assets = CreateRecommendationService.get_user_assets(user)
        CreateRecommendationService.create_new_recommendation(
            user=user, user_assets=user_assets
        )

    @staticmethod
    def create_new_recommendation(user, user_assets):

        """
        The create_new_recommendation function takes in a user and the
         assets that they own.
        It then calculates the average price of all of their assets,
         and finds an asset with a current_price closest to this
          average.
        The relevance value is calculated by dividing the difference
         between these two prices by the average price.

        :param user: Get the user's assets
        :param user_assets: Get the assets that the user already owns
        :return: A recommendation object
        """
        asset_prices = user_assets.values_list('current_price', flat=True)
        avg_price = sum(asset_prices) / len(asset_prices)
        asset_with_min_difference = (
            Asset.objects.annotate(
                difference=Abs(F('current_price') - avg_price)
            )
            .exclude(id__in=user_assets.values('id'))
            .order_by('difference')
            .first()
        )
        relevance_value = asset_with_min_difference.difference / avg_price
        recommendation = Recommendation.objects.create(
            user=user,
            asset=asset_with_min_difference,
            relevance_value=decimal.Decimal(relevance_value),
        )
        return recommendation

    @staticmethod
    def get_user_assets(user):

        """
        The get_user_assets function takes a user as an argument and
         returns all the assets that are associated with that user.
        It does this by querying the Asset model for any asset which
         is either in a portfolio owned by the user, or has been
          recommended to them.
        It then adds to this list of assets any asset which they have
         subscribed to.

        :param user: Filter the assets by user
        :return: A list of the assets that a user is subscribed to
        """
        user_assets = Asset.objects.filter(
            Q(portfolioasset__portfolio__user=user)
            | Q(recommendation__user=user)
        )
        user_assets = user_assets.union(user.subscriptions.all())
        return user_assets
