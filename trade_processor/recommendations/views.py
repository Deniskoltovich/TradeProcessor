from rest_framework import generics, viewsets
from rest_framework.response import Response

from accounts.permissions import IsOwner, IsUser
from mixins.get_serializer_class_mixin import GetSerializerClassMixin
from recommendations.models import Recommendation
from recommendations.serializers import ListRecommendationSerializer
from recommendations.services.get_recommendations_service import (
    GetRecommendationService,
)


class RecommendationViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.DestroyModelMixin,
):
    queryset = Recommendation.objects.all()
    serializer_class = ListRecommendationSerializer

    permission_action_classes = {
        'list': (IsOwner,),
        'retrieve': (IsOwner,),
        'destroy': (IsOwner,),
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (IsUser,)
            )
        ]

    def list(self, request, *args, **kwargs):
        user_recommendations = GetRecommendationService().get_recommendation(
            request.user
        )
        data = ListRecommendationSerializer(
            user_recommendations, many=True
        ).data
        return Response(data)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
