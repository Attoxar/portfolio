# Generated by Django 5.0 on 2024-06-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_remove_order_product_remove_order_quantity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="ordered_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]