# Generated by Django 2.1.1 on 2018-12-20 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_remove_collectionpoint_skincare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='collector',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Collector'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='item',
            name='order_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Employee', verbose_name='Order by Employee'),
        ),
        migrations.AlterField(
            model_name='item',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Service', verbose_name='Package/Order'),
        ),
        migrations.AlterField(
            model_name='orderset',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Coupon', verbose_name='Coupon'),
        ),
        migrations.AlterField(
            model_name='packagesnapshot',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Service', verbose_name='Package'),
        ),
        migrations.AlterField(
            model_name='parentpackage',
            name='emp_pack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_pack_by_employee', to='main.Employee', verbose_name='Packed by Employee'),
        ),
        migrations.AlterField(
            model_name='parentpackage',
            name='emp_split',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emplloyee_splited_package', to='main.Employee', verbose_name='Splitted by Employee'),
        ),
        migrations.AlterField(
            model_name='parentpackage',
            name='order_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.OrderSet', verbose_name='Order Set'),
        ),
        migrations.AlterField(
            model_name='service',
            name='emp_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_created_by_emplloyee', to='main.Employee', verbose_name='Created by Employee'),
        ),
        migrations.AlterField(
            model_name='service',
            name='emp_pack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_repacked_by_employee', to='main.Employee', verbose_name='Packed by Employee'),
        ),
        migrations.AlterField(
            model_name='service',
            name='order_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.OrderSet', verbose_name='Order Set'),
        ),
        migrations.AlterField(
            model_name='service',
            name='parent_package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ParentPackage', verbose_name='Parent Package'),
        ),
        migrations.AlterField(
            model_name='service',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.CoReceiver', verbose_name='Receiver'),
        ),
        migrations.AlterField(
            model_name='service',
            name='ship_to_add',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_to_personal_location', to='main.Address', verbose_name='Shipping Address'),
        ),
        migrations.AlterField(
            model_name='service',
            name='ship_to_col',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_to_collection_point', to='main.CollectionPoint', verbose_name='Shipping Collection Point location'),
        ),
        migrations.AlterField(
            model_name='service',
            name='ship_to_wh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_to_warehouse', to='main.Warehouse', verbose_name='Ship to Warehouse'),
        ),
        migrations.AlterField(
            model_name='service',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='service',
            name='wh_received',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_at_warehouse', to='main.Warehouse', verbose_name='Inter-warehouse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='default_col',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.CollectionPoint', verbose_name='Default Collection Point'),
        ),
    ]
