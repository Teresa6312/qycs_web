# Generated by Django 2.1.1 on 2018-10-02 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_auto_20181001_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionpoint',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Available'),
        ),
    ]
