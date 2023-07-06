import pytest
from django.test import Client, RequestFactory
from rest_framework.test import force_authenticate

from accounts.models import User
from assets.models import Asset
from recommendations.models import Recommendation
from recommendations.views import RecommendationViewSet


@pytest.mark.django_db
class TestRecommendationViewSet:
    #  Tests that a list of recommendations is returned for an authenticated user
    def test_list_recommendations_for_authenticated_user(self, user):
        request = RequestFactory().get('/recommendations/')
        force_authenticate(request, user=user)
        view = RecommendationViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == 200

    #  Tests that a recommendation is retrieved for an authenticated user
    def test_retrieve_recommendation_for_authenticated_user(self, asset, user):
        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=0.5
        )
        request = RequestFactory().get(
            f'/recommendations/{recommendation.id}/'
        )
        force_authenticate(request, user=user)
        view = RecommendationViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=recommendation.id)
        assert response.status_code == 200

    #  Tests that a recommendation is deleted for an authenticated user
    def test_delete_recommendation_for_authenticated_user(
        self, mocker, asset, user
    ):
        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=0.5
        )

        request = RequestFactory().delete(
            f'/recommendations/{recommendation.id}/'
        )
        force_authenticate(request, user=user)
        view = RecommendationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=recommendation.id)
        assert response.status_code == 204

    #  Tests that an unauthenticated user cannot list recommendations
    def test_list_recommendations_for_unauthenticated_user(self):

        # client = Client()
        # response = client.get(f'/recommendations/')
        request = RequestFactory().get('/recommendations/')
        view = RecommendationViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == 403

    #  Tests that an unauthenticated user cannot retrieve a recommendation
    def test_retrieve_recommendation_for_unauthenticated_user(
        self, asset, user
    ):

        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=0.5
        )
        request = RequestFactory().get(
            f'/recommendations/{recommendation.id}/'
        )
        view = RecommendationViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=recommendation.id)
        assert response.status_code == 403

    #  Tests that an unauthenticated user cannot delete a recommendation
    def test_delete_recommendation_for_unauthenticated_user(self, asset, user):

        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=0.5
        )
        request = RequestFactory().delete(
            f'/recommendations/{recommendation.id}/'
        )
        view = RecommendationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=recommendation.id)
        assert response.status_code == 403
