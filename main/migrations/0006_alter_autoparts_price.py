# Generated by Django 4.2.7 on 2023-11-30 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_autoparts_ref_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoparts',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Цена'),
        ),
    ]
