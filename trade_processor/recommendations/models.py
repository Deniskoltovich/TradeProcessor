from django.db import models

from accounts.models import User
from assets.models import Asset

# mypy: ignore-errors


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    relevance_value = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        get_latest_by = "relevance_value"
        constraints = [
            models.CheckConstraint(
                check=models.Q(relevance_value__gte=0),
                name="check_relevance_value_is_positive",
            ),
            models.CheckConstraint(
                check=models.Q(relevance_value__lte=1),
                name="check_relevance_value_is_lte_one",
            ),
        ]

        unique_together = ['user', 'asset']
