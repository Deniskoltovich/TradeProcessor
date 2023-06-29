from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Portfolio
from accounts.permissions import IsAdministrator, IsOwner, IsUser
from accounts.serializers import portfolio_serializers
from accounts.serializers.portfolio_serializers import (
    CreatePortfolioSerializer,
    ListPortfolioSerializer,
    UpdatePortfolioSerializer,
)
from accounts.services.portfolio_service import PortfolioService
from mixins.get_serializer_class_mixin import GetSerializerClassMixin


class PortfolioViewSet(
    viewsets.GenericViewSet,
    generics.mixins.RetrieveModelMixin,
    generics.mixins.ListModelMixin,
    generics.mixins.CreateModelMixin,
    generics.mixins.UpdateModelMixin,
    generics.mixins.DestroyModelMixin,
    GetSerializerClassMixin,
):
    queryset = Portfolio.objects.all()
    serializer_class = portfolio_serializers.ListPortfolioSerializer

    serializer_action_classes = {
        'update': UpdatePortfolioSerializer,
        'partial_update': UpdatePortfolioSerializer,
        'create': CreatePortfolioSerializer,
    }

    permission_action_classes = {
        'list': (IsAdministrator,),
        'retrieve': (IsAdministrator | IsOwner,),
        'update': (IsOwner,),
        'partial_update': (IsOwner,),
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

    @action(detail=False, methods=('get',), url_path='my')  # type: ignore
    def my_portfolios(self, request):

        """
        The my_portfolios function is a GET request that returns all
         the portfolios
        that are associated with the user who made the request. The
         function uses
        the PortfolioService class to find all the portfolios that
         are associated with
        the user who made this request.

        :param self: Represent the instance of the class
        :param request: Get the user from the request object
        :return: A list of all the portfolios that belong to a user
        """
        portfolios = PortfolioService.get_portfolio_by_user(request.user)
        serializer = ListPortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)
