from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Portfolio
from accounts.permissions import IsAdministrator, IsOwner, IsUser
from accounts.serializers import portfolio_serializers
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
    serializer_class = portfolio_serializers.PortfolioSerializer

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
        return Response(
            portfolio_service.PortfolioService().find_my(request.user)
        )
