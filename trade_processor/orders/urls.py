from django.urls import include, path
from orders.views import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
