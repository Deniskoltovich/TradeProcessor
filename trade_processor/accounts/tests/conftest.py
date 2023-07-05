import pytest

from accounts.models import Portfolio, User
from assets.models import Asset


@pytest.fixture
def admin() -> User:
    return User.objects.create_user(
        username='admin',
        email='admin@admin.com',
        password='admin',
        is_superuser=True,
    )


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
