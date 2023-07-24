from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recommendations.views import RecommendationViewSet

router = DefaultRouter()
router.register("", RecommendationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
