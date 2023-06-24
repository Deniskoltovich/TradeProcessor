from assets.models import Asset
from assets.serializers import AssetSerializer


class SubscriptionService:
    @staticmethod
    def list(user):
        return AssetSerializer(user.subscriptions, many=True).data

    @staticmethod
    def add(user, subscription_id):
        asset = Asset.objects.get(id=subscription_id)
        user.subscriptions.add(asset)
        user.save()
        return SubscriptionService.list(user)

    @staticmethod
    def delete(user, subscription_id):
        asset = Asset.objects.get(id=subscription_id)
        user.subscriptions.remove(asset)
        user.save()
        return SubscriptionService.list(user)
