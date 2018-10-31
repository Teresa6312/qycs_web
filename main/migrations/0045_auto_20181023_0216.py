# Generated by Django 2.1.1 on 2018-10-23 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_auto_20181022_1146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name_plural': 'Location'},
        ),
        migrations.AlterModelOptions(
            name='pricerate',
            options={'verbose_name_plural': 'Price Rate'},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'verbose_name_plural': 'Resource'},
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='apply_reason',
            field=models.TextField(blank=True, default='', verbose_name='Apply reason'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='info_source',
            field=models.CharField(blank=True, choices=[('WC', 'WeChat'), ('DM', 'Dealmoon')], default='', max_length=100, verbose_name='Information source'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='license_type',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='License type'),
        ),
    ]
