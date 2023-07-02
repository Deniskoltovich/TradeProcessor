from assets.models import Asset
from assets.serializers import AssetSerializer
from recommendations.services.create_recommendation_service import (
    CreateRecommendationService,
)


class SubscriptionService:
    @staticmethod
    def add(user, subscription_id):

        """
        The add function adds a subscription to the user's list of
         subscriptions.

        :param user: Identify the user that is adding a subscription
        :param subscription_id: Get the asset object from the database
        :return: The list of subscriptions for the user
        """
        asset = Asset.objects.get(id=subscription_id)
        user.subscriptions.add(asset)
        user.save()
        CreateRecommendationService.execute(asset=asset, user=user)
        return user.subscriptions

    @staticmethod
    def delete(user, subscription_id):

        """
        The delete function gets the asset with the given id, removes
         it from the user's subscriptions

        :param user: Get the user's subscriptions
        :param subscription_id: Find the asset that is being deleted
        :return: A list of the user's subscriptions
        """
        asset = Asset.objects.get(id=subscription_id)
        user.subscriptions.remove(asset)
        user.save()
        return user.subscriptions
