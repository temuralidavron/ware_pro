# Generated by Django 5.1.7 on 2025-03-26 06:23

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_product_quantity_alter_transaction_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15),
        ),
    ]
