import decimal

from assets.models import Asset


class PriceService:
    @staticmethod
    def update_price(asset_data: dict):
        print(asset_data)
        print(type(asset_data))
        asset = Asset.objects.get(name=asset_data['name'])
        asset.current_price = decimal.Decimal(asset_data["current_price"])
        asset.save()
        return asset
