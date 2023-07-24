from django.urls import include, path
from rest_framework.routers import DefaultRouter

from assets.views import AssetViewSet

router = DefaultRouter()
router.register("", AssetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
