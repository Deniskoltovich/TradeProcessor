import pytest
from django.db import IntegrityError

from assets.models import Asset


@pytest.mark.django_db
class TestAsset:
    #  Tests that an Asset object can be created with all required fields
    def test_create_asset_with_all_fields(self):
        asset = Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        assert asset.name == 'Bitcoin'
        assert asset.logo_url == 'https://bitcoin.org/img/icons/opengraph.png'
        assert asset.description == 'A decentralized digital currency'
        assert asset.type == Asset.Type.CRYPTOCURRENCY
        assert asset.current_price == 50000

    #  Tests that an Asset object can be updated with valid data
    def test_update_asset_with_valid_data(self):
        asset = Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        asset.name = 'Ethereum'
        asset.logo_url = 'https://ethereum.org/favicon.ico'
        asset.description = (
            'A blockchain-based decentralized software platform'
        )
        asset.type = Asset.Type.SHARE
        asset.current_price = 3000
        asset.save()
        updated_asset = Asset.objects.get(id=asset.id)
        assert updated_asset.name == 'Ethereum'
        assert updated_asset.logo_url == 'https://ethereum.org/favicon.ico'
        assert (
            updated_asset.description
            == 'A blockchain-based decentralized software platform'
        )
        assert updated_asset.type == Asset.Type.SHARE
        assert updated_asset.current_price == 3000

    #  Tests that an Asset object can be deleted
    def test_delete_asset(self):
        asset = Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        asset.delete()
        with pytest.raises(Asset.DoesNotExist):
            Asset.objects.get(id=asset.id)

    #  Tests that an Asset object cannot be created with a name that already exists
    def test_create_asset_with_existing_name(self):
        Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        with pytest.raises(IntegrityError):
            Asset.objects.create(
                name='Bitcoin',
                logo_url='https://bitcoin.org/img/icons/opengraph.png',
                description='A decentralized digital currency',
                type=Asset.Type.CRYPTOCURRENCY,
                current_price=50000,
            )

    #  Tests that an Asset object cannot be created with a negative current price
    def test_create_asset_with_negative_current_price(self):
        with pytest.raises(IntegrityError):
            Asset.objects.create(
                name='Apple',
                logo_url='https://apple.com/favicon.ico',
                description='A technology company',
                type=Asset.Type.SHARE,
                current_price=-150,
            )

    #  Tests that an Asset object cannot be updated with a negative current price
    def test_update_asset_with_negative_current_price(self):
        asset = Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        with pytest.raises(IntegrityError):
            asset.current_price = -1000
            asset.save()

    #  Tests that an Asset object can be retrieved by name
    def test_retrieve_asset_by_name(self):
        Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        asset = Asset.objects.get(name='Bitcoin')
        assert asset.name == 'Bitcoin'
        assert asset.logo_url == 'https://bitcoin.org/img/icons/opengraph.png'
        assert asset.description == 'A decentralized digital currency'
        assert asset.type == Asset.Type.CRYPTOCURRENCY
        assert asset.current_price == 50000

    #  Tests that all Asset objects can be retrieved
    def test_retrieve_all_assets(self):
        Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        Asset.objects.create(
            name='Ethereum',
            logo_url='https://ethereum.org/favicon.ico',
            description='A blockchain-based decentralized software platform',
            type=Asset.Type.SHARE,
            current_price=3000,
        )
        assets = Asset.objects.all()
        assert len(assets) == 2

    #  Tests that all Asset objects of a certain type can be retrieved
    def test_retrieve_assets_by_type(self):
        Asset.objects.create(
            name='Bitcoin',
            logo_url='https://bitcoin.org/img/icons/opengraph.png',
            description='A decentralized digital currency',
            type=Asset.Type.CRYPTOCURRENCY,
            current_price=50000,
        )
        Asset.objects.create(
            name='Ethereum',
            logo_url='https://ethereum.org/favicon.ico',
            description='A blockchain-based decentralized software platform',
            type=Asset.Type.SHARE,
            current_price=3000,
        )
        crypto_assets = Asset.objects.filter(type=Asset.Type.CRYPTOCURRENCY)
        assert len(crypto_assets) == 1
        assert crypto_assets[0].name == 'Bitcoin'
        assert crypto_assets[0].type == Asset.Type.CRYPTOCURRENCY
        share_assets = Asset.objects.filter(type=Asset.Type.SHARE)
        assert len(share_assets) == 1
        assert share_assets[0].name == 'Ethereum'
        assert share_assets[0].type == Asset.Type.SHARE
