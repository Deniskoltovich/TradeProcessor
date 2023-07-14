# Generated by Django 4.2.3 on 2023-07-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(("balance__gte", 0)),
                name="check_balance_is_positive"
            ),
        ),
    ]