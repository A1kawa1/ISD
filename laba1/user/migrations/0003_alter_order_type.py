# Generated by Django 3.2.18 on 2023-02-18 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_lost_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[('наличный расчет', 'наличный расчет'), ('безналичный расчет', 'безналичный расчет'), ('кредит', 'кредит'), ('бартер', 'бартер')], default=None, max_length=50),
        ),
    ]
