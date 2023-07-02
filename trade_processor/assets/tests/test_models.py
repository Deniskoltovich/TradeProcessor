from assets.models import Asset
from django.db.utils import IntegrityError
from django.test import TestCase


class TestAssetModels(TestCase):
    def setUp(self) -> None:
        self.asset = Asset.objects.create(
            name='Bitcoin', type=Asset.Type.CRYPTOCURRENCY
        )
        return super().setUp()

    def test_asset_assigning_default_values(self):
        asset = Asset.objects.create(
            name='Some coin', type=Asset.Type.CRYPTOCURRENCY
        )
        assert asset.logo_url is None
        assert asset.description == ""

    def test_unique_asset_name(self):
        with self.assertRaises(IntegrityError):
            Asset.objects.create(name='Bitcoin', type=Asset.Type.SHARE)

    def test_required_name_field(self):
        with self.assertRaises(IntegrityError):
            Asset.objects.create(type=Asset.Type.CRYPTOCURRENCY)

    def test_required_type_field(self):
        with self.assertRaises(IntegrityError):
            Asset.objects.create(name='some name')
