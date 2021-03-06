# Generated by Django 2.0.7 on 2018-09-10 17:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180910_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.CharField(default='', max_length=12, validators=[django.core.validators.RegexValidator(message='Plese Enter a valid zip code.', regex='^[0-9]{2,6}(?:-[0-9]{4})?$|^$')], verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='zipcode',
            field=models.CharField(default='', max_length=12, validators=[django.core.validators.RegexValidator(message='Plese Enter a valid zip code.', regex='^[0-9]{2,6}(?:-[0-9]{4})?$|^$')], verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='zipcode',
            field=models.CharField(default='', max_length=12, validators=[django.core.validators.RegexValidator(message='Plese Enter a valid zip code.', regex='^[0-9]{2,6}(?:-[0-9]{4})?$|^$')], verbose_name='Zip Code'),
        ),
    ]
