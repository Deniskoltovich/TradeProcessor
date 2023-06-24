from django.db import transaction
from orders.serializers import CreateOrderSerializer


class OrderCreateService:
    @staticmethod
    def execute(data):
        serializer = CreateOrderSerializer(data=data)
        serializer.is_valid()

        asset = serializer.validated_data.get('asset')
        portfolio = serializer.validated_data.get('portfolio')
        with transaction.atomic():
            portfolio.assets.add(asset)
            portfolio.save()
            serializer.save()
            return serializer.data
