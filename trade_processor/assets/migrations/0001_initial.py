# Generated by Django 4.2.2 on 2023-06-22 07:34

from django.db import migrations, models

# mypy: ignore-errors

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asset",
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
                ("name", models.CharField(max_length=64, unique=True)),
                ("logo_url", models.CharField(default=None, max_length=255, null=True)),
                ("description", models.TextField(blank=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Cryptocurrency", "Cryptocurrency"),
                            ("Share", "Share"),
                        ],
                        max_length=14,
                    ),
                ),
            ],
        ),
    ]