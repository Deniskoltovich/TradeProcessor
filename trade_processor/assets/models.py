from django.db import models


class Asset(models.Model):
    class Type(models.TextChoices):
        CREPTOCURRENCY = 'Сryptocurrency'
        SHARE = 'Share'

    name: str = models.CharField(max_length=64, unique=True, null=False)
    logo_url: str = models.CharField(max_length=255, unique=True, default=None)
    description: str = models.TextField()
    type: str = models.CharField(max_length=14, choices=Type.choices)
