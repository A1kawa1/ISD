# Generated by Django 4.1.7 on 2023-05-15 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0012_alter_accessories_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessories',
            name='count',
            field=models.PositiveIntegerField(verbose_name='Количество'),
        ),
    ]
