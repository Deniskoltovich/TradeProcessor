# Generated by Django 4.2.2 on 2023-06-28 10:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("assets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recommendation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "relevance_value",
                    models.DecimalField(decimal_places=4, max_digits=5),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="assets.asset"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "get_latest_by": "relevance_value",
                "unique_together": {("user", "asset")},
            },
        ),
    ]
