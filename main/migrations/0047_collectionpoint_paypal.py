# Generated by Django 2.1.1 on 2018-10-23 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_auto_20181023_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionpoint',
            name='paypal',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Paypal account'),
        ),
    ]