# Generated by Django 4.1.7 on 2023-05-15 15:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0011_assemblyorder_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessories',
            name='count',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Минимальное количество - 1')], verbose_name='Количество'),
        ),
    ]
