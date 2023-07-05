import django
import pytest
from django.db import IntegrityError

from accounts.models import Portfolio, User
from assets.models import Asset


@pytest.mark.django_db
class TestPortfolio:
    #  Tests that a new portfolio can be created with a user and assets
    def test_create_portfolio_with_user_and_assets(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        asset1 = Asset.objects.create(
            name='asset1', current_price=10.0, type=Asset.Type.SHARE
        )
        asset2 = Asset.objects.create(
            name='asset2', current_price=10.0, type=Asset.Type.SHARE
        )
        portfolio = Portfolio.objects.create(user=user, name='test_portfolio')
        portfolio.assets.add(asset1, asset2)
        assert portfolio.assets.count() == 2

    #  Tests that assets can be added to an existing portfolio
    def test_add_assets_to_existing_portfolio(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        asset1 = Asset.objects.create(
            name='asset1', current_price=10.0, type=Asset.Type.SHARE
        )
        asset2 = Asset.objects.create(
            name='asset2', current_price=10.0, type=Asset.Type.SHARE
        )
        portfolio = Portfolio.objects.create(user=user, name='test_portfolio')
        portfolio.assets.add(asset1)
        portfolio.assets.add(asset2)
        assert portfolio.assets.count() == 2

    #  Tests that the name and description of a portfolio can be updated
    def test_update_portfolio_name_and_description(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        portfolio = Portfolio.objects.create(user=user, name='test_portfolio')
        portfolio.description = 'new description'
        portfolio.name = 'new name'
        portfolio.save()
        assert portfolio.description == 'new description'
        assert portfolio.name == 'new name'

    #  Tests that assets can be removed from a portfolio
    def test_remove_assets_from_portfolio(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        asset1 = Asset.objects.create(
            name='asset1', current_price=10.0, type=Asset.Type.SHARE
        )
        asset2 = Asset.objects.create(
            name='asset2', current_price=10.0, type=Asset.Type.SHARE
        )
        portfolio = Portfolio.objects.create(user=user, name='test_portfolio')
        portfolio.assets.add(asset1, asset2)
        portfolio.assets.remove(asset1)
        assert portfolio.assets.count() == 1

    def test_create_portfolio_with_long_name(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        with pytest.raises(django.db.utils.DataError):
            Portfolio.objects.create(user=user, name='a' * 65)

    def test_create_portfolio_with_long_description(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        Portfolio.objects.create(
            user=user, name='test_portfolio', description='a' * 256
        )

    #  Tests that all portfolios for a user can be retrieved
    def test_get_all_portfolios_for_user(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        portfolio1 = Portfolio.objects.create(
            user=user, name='test_portfolio1'
        )
        portfolio2 = Portfolio.objects.create(
            user=user, name='test_portfolio2'
        )
        portfolios = Portfolio.objects.filter(user=user)
        assert len(portfolios) == 2
        assert portfolio1 in portfolios
        assert portfolio2 in portfolios

    #  Tests that all assets for a portfolio can be retrieved
    def test_get_all_assets_for_portfolio(self):
        user = User.objects.create(
            username='test_user', email='test_user@example.com'
        )
        asset1 = Asset.objects.create(
            name='asset1', current_price=10.0, type=Asset.Type.SHARE
        )
        asset2 = Asset.objects.create(
            name='asset2', current_price=10.0, type=Asset.Type.SHARE
        )
        portfolio = Portfolio.objects.create(user=user, name='test_portfolio')
        portfolio.assets.add(asset1, asset2)
        assets = portfolio.assets.all()
        assert len(assets) == 2
        assert asset1 in assets
        assert asset2 in assets
