from assets.views import AssetViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", AssetViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
