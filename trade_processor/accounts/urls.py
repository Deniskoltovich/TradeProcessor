from accounts.views import PortfolioViewSet, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("portfolios", PortfolioViewSet)
router.register("", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
