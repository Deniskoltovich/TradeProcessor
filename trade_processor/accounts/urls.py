from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views.portfolio_views import PortfolioViewSet
from accounts.views.user_views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("portfolios", PortfolioViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
