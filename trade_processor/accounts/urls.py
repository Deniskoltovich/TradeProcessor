from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views.portfolio_views import PortfolioViewSet
from accounts.views.user_views import UserViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register("users", UserViewSet, basename='users')
router.register("portfolios", PortfolioViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
