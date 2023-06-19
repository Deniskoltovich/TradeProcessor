from assets.models import Asset
from django.contrib.auth.models import AbstractUser
from django.db import models
from mixins.models import EditCreationDateMixinModel


class CustomUser(AbstractUser, EditCreationDateMixinModel):
    class Role(models.TextChoices):
        ADMIN = 'Admin'
        ANALYST = 'Analyst'
        USER = 'User'

    class Status(models.TextChoices):
        ACTIVE = 'Active'
        DEACTIVE = 'Deactive'

    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=Role.choices, default=Role.USER)
    avatar_url = models.CharField(max_length=255, unique=True, default=None)
    subscriptions = models.ManyToManyField(Asset)
    status = models.IntegerField(
        choices=Status.choices, default=Status.DEACTIVE
    )
    balance = models.PositiveIntegerField(default=0)


class Portfolio(EditCreationDateMixinModel):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Asset)
    name = models.CharField(max_length=64, default="My portfolio")
    description = models.TextField(blank=True)
