from accounts.models import Portfolio
from assets.models import Asset
from django.db import models
from mixins.models import EditCreationDateMixinModel


class Order(EditCreationDateMixinModel):
    class OperationType(models.TextChoices):
        SELL = 'Sell'
        BUY = 'Buy'

    class Status(models.TextChoices):
        FINISHED = 'Finished'
        CANCELLED = 'Cancelled'

    class INITIALIZER(models.TextChoices):
        AUTO = 'Auto'
        MANUAL = 'Manual'

    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    initializer = models.CharField(max_length=6, choices=INITIALIZER.choices)
    operation_type = models.CharField(
        max_length=4, choices=OperationType.choices
    )
    price = models.DecimalField(max_digits=11, decimal_places=2, blank=False)
    quantity = models.IntegerField(blank=False)
    status = models.CharField(max_length=9, choices=Status.choices)


class AutoOrder(EditCreationDateMixinModel):
    class OperationType(models.TextChoices):
        SELL = 'Sell'
        BUY = 'Buy'

    class Status(models.TextChoices):
        FINISHED = 'Finished'
        CANCELLED = 'Cancelled'
        OPENED = 'Opened'

    class PriceDirection(models.TextChoices):
        HIGHER = 'Higher'
        LOWER = 'Lower'

    portfolio_id = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    operation_type = models.CharField(
        max_length=4, choices=OperationType.choices
    )

    desired_price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=False
    )
    quantity = models.IntegerField(blank=False)

    price_direction = models.CharField(
        choices=PriceDirection.choices, max_length=6
    )
    status = models.CharField(max_length=9, choices=Status.choices)
