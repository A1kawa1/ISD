# Generated by Django 3.2.18 on 2023-02-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230211_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=12, verbose_name='Телефон'),
        ),
    ]
