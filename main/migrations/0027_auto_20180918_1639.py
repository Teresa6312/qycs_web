# Generated by Django 2.0.7 on 2018-09-18 16:39

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20180918_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionpoint',
            name='collector_icon',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='collector_icon'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='license_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='collector_license'),
        ),
    ]