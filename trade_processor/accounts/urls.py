from django.urls import include, path
from recommendations.views import RecommendationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", RecommendationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
