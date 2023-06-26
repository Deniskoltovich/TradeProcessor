# Generated by Django 4.2.2 on 2023-06-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_alter_autoorder_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-updated_at", "-created_at"]},
        ),
        migrations.AlterField(
            model_name="autoorder",
            name="operation_type",
            field=models.CharField(
                choices=[("Sell", "Sell"), ("Buy", "Buy")], default=None, max_length=4
            ),
        ),
        migrations.AlterField(
            model_name="autoorder",
            name="price_direction",
            field=models.CharField(
                choices=[("Higher", "Higher"), ("Lower", "Lower")],
                default=None,
                max_length=6,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="operation_type",
            field=models.CharField(
                choices=[("Sell", "Sell"), ("Buy", "Buy")], default=None, max_length=4
            ),
        ),
    ]