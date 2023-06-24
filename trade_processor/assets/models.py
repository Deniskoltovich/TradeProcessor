from django.db import models

# mypy: ignore-errors


class Asset(models.Model):
    class Type(models.TextChoices):
        CRYPTOCURRENCY = "Cryptocurrency"
        SHARE = "Share"

    name: str = models.CharField(
        max_length=64, unique=True, null=False, default=None
    )
    logo_url: str = models.CharField(max_length=255, null=True, default=None)
    description: str = models.TextField(blank=True)
    type: str = models.CharField(
        max_length=14, choices=Type.choices, null=False, default=None
    )

    def __str__(self):
        return self.name
