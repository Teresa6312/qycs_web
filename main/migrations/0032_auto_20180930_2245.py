# Generated by Django 2.1.1 on 2018-09-30 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_user_privacy_policy_agree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionpoint',
            name='wechat',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='WeChat ID'),
        ),
    ]
