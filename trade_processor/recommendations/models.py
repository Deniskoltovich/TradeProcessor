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
        unique_together = ['user', 'asset']
