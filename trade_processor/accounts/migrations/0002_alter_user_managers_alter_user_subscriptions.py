# Generated by Django 4.2.2 on 2023-06-22 09:50

from django.db import migrations, models

# mypy: ignore-errors


class Migration(migrations.Migration):
    dependencies = [
        ("assets", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.AlterField(
            model_name="user",
            name="subscriptions",
            field=models.ManyToManyField(blank=True, to="assets.asset"),
        ),
    ]
