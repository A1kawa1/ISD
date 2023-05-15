# Generated by Django 4.1.7 on 2023-05-15 12:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0006_rename_ingredient_assemblyorderaccessories_accessories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assemblyorderaccessories',
            name='count',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Минимальное количество - 1')], verbose_name='Количество'),
        ),
    ]