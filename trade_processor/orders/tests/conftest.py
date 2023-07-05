import pytest

from accounts.models import Portfolio, User
from assets.models import Asset


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username='user', password='password', email="use@d.com"
    )


@pytest.fixture
def asset() -> Asset:
    asset = Asset.objects.create(
        name='Bitcoin',
        logo_url='https://bitcoin.org/img/icons/opengraph.png',
        description='A decentralized digital currency',
        type=Asset.Type.CRYPTOCURRENCY,
        current_price=50000,
    )
    return asset


@pytest.fixture
def portfolio() -> Portfolio:
    portfolio = Portfolio.objects.create(
        user=User.objects.create_user(
            'user@d.com', 'password', username='username'
        ),
    )
    asset = Asset.objects.create(
        name='asset1', type=Asset.Type.CRYPTOCURRENCY, current_price=10.00
    )
    portfolio.assets.add(asset)
    return portfolio
