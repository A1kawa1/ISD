# Generated by Django 4.1.7 on 2023-05-15 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0002_assemblyorder_alter_accessories_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assemblyorderaccessories',
            options={'verbose_name': 'Комплектующее', 'verbose_name_plural': 'Комплектующие'},
        ),
    ]
