from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager
from assets.models import Asset
from mixins.base_model import EditCreationDateMixinModel

# mypy: ignore-errors


class User(AbstractUser, EditCreationDateMixinModel):
    class Role(models.TextChoices):
        ADMIN = "Admin"
        ANALYST = "Analyst"
        USER = "User"

    class Status(models.TextChoices):
        ACTIVE = "Active"
        INACTIVE = "Inactive"

    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(
        choices=Role.choices, default=Role.USER, max_length=7
    )
    avatar_url = models.CharField(max_length=255, null=True, default=None)
    subscriptions = models.ManyToManyField(Asset, blank=True)
    status = models.CharField(
        choices=Status.choices, default=Status.INACTIVE, max_length=9
    )
    balance = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.00
    )

    objects = UserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=0),
                name="check_balance_is_positive",
            )
        ]


class Portfolio(EditCreationDateMixinModel):
    user = models.ForeignKey(
        User, related_name="portfolios", on_delete=models.CASCADE
    )
    assets = models.ManyToManyField(
        Asset, through='PortfolioAsset', verbose_name='Assets'
    )
    name = models.CharField(max_length=64, default="My portfolio")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user}'s portfolio"


class PortfolioAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
