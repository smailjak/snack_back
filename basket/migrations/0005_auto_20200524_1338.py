# Generated by Django 3.0.3 on 2020-05-24 13:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0004_order_is_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_summary',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order_amount',
            field=models.PositiveSmallIntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)]),
        ),
    ]