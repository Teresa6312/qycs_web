# Generated by Django 2.1.1 on 2018-10-03 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_auto_20181002_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionpoint',
            name='wechat',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='WeChat ID'),
        ),
    ]
