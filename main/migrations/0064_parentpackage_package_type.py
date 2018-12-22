# Generated by Django 2.1.1 on 2018-12-22 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0063_parentpackage_volume_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentpackage',
            name='package_type',
            field=models.CharField(blank=True, choices=[('B-F', 'Food/Grocery'), ('A-R', 'Regular Goods'), ('C-B', 'Beauty'), ('D-L', 'Luxury'), ('E-M', 'Mix')], default='', max_length=16, verbose_name='Package Type'),
        ),
    ]
