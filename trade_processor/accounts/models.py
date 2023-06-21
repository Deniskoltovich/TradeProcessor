from assets.models import Asset
from django.contrib.auth.models import AbstractUser
from django.db import models
from mixins.models import EditCreationDateMixinModel


class User(AbstractUser, EditCreationDateMixinModel):
    class Role(models.TextChoices):
        ADMIN = 'Admin'
        ANALYST = 'Analyst'
        USER = 'User'

    class Status(models.TextChoices):
        ACTIVE = 'Active'
        INACTIVE = 'Inactive'

    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=Role.choices, default=Role.USER, max_length=7
    )
    avatar_url = models.CharField(max_length=255, null=True, default=None)
    subscriptions = models.ManyToManyField(Asset)
    status = models.CharField(
        choices=Status.choices, default=Status.INACTIVE, max_length=9
    )
    balance = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.00
    )


class Portfolio(EditCreationDateMixinModel):
    user = models.ForeignKey(
        User, related_name='portfolios', on_delete=models.CASCADE
    )
    assets = models.ManyToManyField(Asset)
    name = models.CharField(max_length=64, default="My portfolio")
    description = models.TextField(blank=True)
