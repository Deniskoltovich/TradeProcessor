from django.db import models


class Asset(models.Model):
    class Type(models.TextChoices):
        CRYPTOCURRENCY = 'Cryptocurrency'
        SHARE = 'Share'

    name: str = models.CharField(max_length=64, unique=True, null=False)
    logo_url: str = models.CharField(max_length=255, null=True, default=None)
    description: str = models.TextField(blank=True)
    type: str = models.CharField(max_length=14, choices=Type.choices)
