import pytest
from django.db.utils import IntegrityError

from accounts.models import User
from assets.models import Asset
from recommendations.models import Recommendation


@pytest.mark.django_db
class TestRecommendation:
    #  Tests that a new Recommendation instance can be created with valid user, asset and relevance_value
    def test_create_recommendation_with_valid_user_asset_and_relevance_value(
        self, user, asset
    ):
        # Arrange
        relevance_value = 0.5

        # Act
        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=relevance_value
        )

        # Assert
        assert recommendation.user == user
        assert recommendation.asset == asset
        assert recommendation.relevance_value == relevance_value

    #  Tests that a Recommendation instance can be retrieved by its primary key
    def test_retrieve_recommendation_by_primary_key(self, user, asset):
        # Arrange

        relevance_value = 0.5
        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=relevance_value
        )

        # Act
        retrieved_recommendation = Recommendation.objects.get(
            pk=recommendation.pk
        )

        # Assert
        assert retrieved_recommendation == recommendation

    #  Tests that a Recommendation instance can be updated with valid relevance_value
    def test_update_recommendation_with_valid_relevance_value(
        self, user, asset
    ):
        # Arrange

        relevance_value = 0.5
        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=relevance_value
        )
        new_relevance_value = 0.7

        # Act
        recommendation.relevance_value = new_relevance_value
        recommendation.save()

        # Assert
        assert recommendation.relevance_value == new_relevance_value

    #  Tests that a Recommendation instance can be deleted
    def test_delete_recommendation(self, user, asset):
        # Arrange

        relevance_value = 0.5
        recommendation = Recommendation.objects.create(
            user=user, asset=asset, relevance_value=relevance_value
        )

        # Act
        recommendation.delete()

        # Assert
        with pytest.raises(Recommendation.DoesNotExist):
            Recommendation.objects.get(pk=recommendation.pk)

    def test_create_recommendation_with_invalid_relevance_value1(
        self, user, asset
    ):

        # Act & Assert
        with pytest.raises(IntegrityError):
            Recommendation.objects.create(
                user=user, asset=asset, relevance_value=-0.1
            )

    def test_create_recommendation_with_invalid_relevance_value2(
        self, user, asset
    ):

        with pytest.raises(IntegrityError):
            Recommendation.objects.create(
                user=user, asset=asset, relevance_value=1.1
            )
