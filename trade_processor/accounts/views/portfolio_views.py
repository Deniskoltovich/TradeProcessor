from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts import serializers
from accounts.models import Portfolio
from accounts.permissions import IsAdministrator, IsOwner, IsUser
from accounts.services import portfolio_service


class PortfolioViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.DestroyModelMixin,
):
    queryset = Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer

    permission_action_classes = {
        'list': (IsAdministrator,),
        'retrieve': (IsAdministrator | IsOwner,),
        'update': (IsAdministrator,),
        'partial_update': (IsAdministrator,),
        'destroy': (IsAdministrator | IsOwner,),
        'create': (IsAdministrator | IsUser,),
        'my_portfolios': (IsUser,),
    }

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_action_classes.get(
                self.action, (IsUser,)
            )
        ]

    @action(detail=False, methods=['get'], url_path='my')
    def my_portfolios(self, request):
        return Response(
            portfolio_service.PortfolioService().find_my(request.user)
        )
