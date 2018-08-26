# Generated by Django 2.0.7 on 2018-08-26 21:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=500, verbose_name='地址')),
                ('apt', models.CharField(blank=True, default='', max_length=10, verbose_name='Apartment')),
                ('city', models.CharField(default='', max_length=100, verbose_name='City')),
                ('state', models.CharField(default='', max_length=100, verbose_name='State')),
                ('country', models.CharField(default='', max_length=100, verbose_name='Country')),
                ('zipcode', models.CharField(default='', max_length=5, verbose_name='Zip Code')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Address Meno')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Last Name')),
                ('phone', models.CharField(blank=True, default='', max_length=16, validators=[django.core.validators.RegexValidator(message="Invalid phone number format. Enter as 123-456-0987. Optionally enter extensions using 'x' followed by the number.", regex='^\\s*(?:\\+?(\\d{1,3}))?[-. (]*(\\d{3})[-. )]*(\\d{3})[-. ]*(\\d{4})(?: *x(\\d+))?\\s*$')], verbose_name='Phone Number')),
                ('email', models.EmailField(blank=True, default='', max_length=100, verbose_name='Email Address')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_num', models.CharField(default='', max_length=16, unique=True, verbose_name='Card Number')),
                ('card_exp', models.CharField(default='', max_length=6, verbose_name='Expiration Date(MM/YY)')),
                ('card_security_code', models.CharField(default='', max_length=6, verbose_name='Security Code')),
                ('address', models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='main.Address', verbose_name='Address')),
            ],
        ),
        migrations.CreateModel(
            name='CollectionPoint',
            fields=[
                ('address', models.CharField(default='', max_length=500, verbose_name='地址')),
                ('apt', models.CharField(blank=True, default='', max_length=10, verbose_name='Apartment')),
                ('city', models.CharField(default='', max_length=100, verbose_name='City')),
                ('state', models.CharField(default='', max_length=100, verbose_name='State')),
                ('country', models.CharField(default='', max_length=100, verbose_name='Country')),
                ('zipcode', models.CharField(default='', max_length=5, verbose_name='Zip Code')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Address Meno')),
                ('collector', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Collector')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(default='', max_length=16, unique=True, verbose_name='Collection Point Name')),
                ('license', models.CharField(default='', max_length=32, verbose_name='License Number')),
                ('license_type', models.CharField(default='', max_length=32, verbose_name='License Type')),
                ('license_image', models.ImageField(blank='True', upload_to='collector_license')),
                ('id_image', models.ImageField(default='', upload_to='collector_id')),
                ('store_name', models.CharField(default='', max_length=16, unique=True, verbose_name='Store Name')),
                ('store', models.BooleanField(default=True, verbose_name='Store')),
                ('status', models.BooleanField(default=False, verbose_name='Avaliable')),
                ('location_image', models.ImageField(blank='True', upload_to='collector_image')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('dimension', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('food', models.BooleanField(default=False)),
                ('regular', models.BooleanField(default=False)),
                ('luxury', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='', max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Last Point Name')),
                ('phone', models.CharField(blank=True, default='', max_length=25, validators=[django.core.validators.RegexValidator(message="Invalid phone number format. Enter as 123-456-0987. Optionally enter extensions using 'x' followed by the number.", regex='^\\s*(?:\\+?(\\d{1,3}))?[-. (]*(\\d{3})[-. )]*(\\d{3})[-. ]*(\\d{4})(?: *x(\\d+))?\\s*$')], verbose_name='Phone Number')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('code', models.CharField(default='', max_length=16, unique=True, verbose_name='Coupon Code')),
                ('discount', models.PositiveIntegerField(default=5, verbose_name='Discount')),
                ('amount_limit', models.PositiveIntegerField(blank=True, null=True, verbose_name='Amount Limit')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Start on')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='End on')),
                ('package', models.BooleanField(default=False, verbose_name='Good For Package')),
                ('order', models.BooleanField(default=False, verbose_name='Good For Order')),
                ('one_time_only', models.BooleanField(default=True, verbose_name='One Time Use Only')),
                ('used_times', models.PositiveIntegerField(default=0, verbose_name='Coupon Used Times')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Memo')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('position', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteWebsite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, default='', max_length=100, verbose_name='Country')),
                ('web_type', models.CharField(blank=True, choices=[('Clothing', 'Clothing'), ('Bag', 'Bag'), ('Jewelry', 'Jewelry'), ('Sport', 'Sport'), ('Beauty', 'Beauty'), ('Baby', 'Baby'), ('Other', 'Other')], default='', max_length=32, verbose_name='Websit Type')),
                ('web_name', models.CharField(blank=True, default='', max_length=64, verbose_name='Websit Name')),
                ('web_url', models.URLField(blank=True, default='', max_length=128, verbose_name='Websit url')),
                ('rate', models.PositiveIntegerField(default=1, verbose_name='Rate')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='', max_length=100, verbose_name='Item Name')),
                ('item_detail', models.CharField(blank=True, default='', max_length=100, verbose_name='Item Details')),
                ('item_quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('item_value', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Item Value')),
                ('currency', models.CharField(blank=True, default='', max_length=16, verbose_name='Currency')),
                ('tax_included', models.BooleanField(default=True, verbose_name='Included Tax')),
                ('item_url', models.CharField(blank=True, default='', max_length=1000, verbose_name='Item URL')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Memo')),
                ('low_volume_request', models.BooleanField(default=True, verbose_name='Low Volume Request')),
                ('issue', models.TextField(blank=True, default='', verbose_name='Item Issue')),
                ('order_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Employee', verbose_name='Order by Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('city', models.CharField(blank=True, default='', max_length=100)),
                ('state', models.CharField(blank=True, default='', max_length=100)),
                ('country', models.CharField(blank=True, default='', max_length=100)),
                ('country_sortname', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OtherPayMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('Alipay', 'Alipay'), ('Paypal', 'Paypal'), ('WeChat', 'WeChat')], max_length=10, verbose_name='Method')),
                ('email', models.EmailField(blank=True, default='', max_length=100, verbose_name='Email Address')),
                ('phone', models.CharField(blank=True, default='', max_length=16, validators=[django.core.validators.RegexValidator(message="Invalid phone number format. Enter as 123-456-0987. Optionally enter extensions using 'x' followed by the number.", regex='^\\s*(?:\\+?(\\d{1,3}))?[-. (]*(\\d{3})[-. )]*(\\d{3})[-. ]*(\\d{4})(?: *x(\\d+))?\\s*$')], verbose_name='Phone Number')),
                ('account_id', models.CharField(blank=True, default='', max_length=64, verbose_name='Account Id')),
                ('account_name', models.CharField(blank=True, default='', max_length=64, verbose_name='Account Name')),
            ],
            options={
                'verbose_name_plural': 'Other Pay Method',
            },
        ),
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='package_snapshot')),
            ],
        ),
        migrations.CreateModel(
            name='ParentPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('packed_date', models.DateField(blank=True, null=True, verbose_name='Packed on')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Memo')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Weight(kg)')),
                ('tracking_num', models.CharField(blank=True, default='', max_length=32, verbose_name='Tracking Number')),
                ('carrier', models.CharField(blank=True, default='', max_length=32, verbose_name='Carrier')),
                ('shipped_date', models.DateField(blank=True, null=True, verbose_name='Shipped on')),
                ('received_date', models.DateField(blank=True, null=True, verbose_name='Received on')),
                ('status', models.CharField(blank=True, default='', max_length=100, verbose_name='Status')),
                ('issue', models.TextField(blank=True, default='', verbose_name='Accident Memo')),
                ('emp_pack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='package_pack_by_employee', to='main.Employee', verbose_name='Packed by Employee')),
                ('emp_split', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='emplloyee_splited_package', to='main.Employee', verbose_name='Splitted by Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Pay on')),
                ('transaction_id', models.CharField(default='', max_length=32, unique=True, verbose_name='Payment Confirmation')),
                ('deposit', models.BooleanField(default=False, verbose_name='Deposit')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Paid Amount')),
                ('currency', models.CharField(default='', max_length=32, verbose_name='Currency')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Memo')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Coupon', verbose_name='Coupon')),
                ('pay_by_card', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='main.Card', verbose_name='Card Payment Id')),
                ('pay_by_other', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.OtherPayMethod', verbose_name='Other Payment Id')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.BooleanField(default=False, verbose_name='Order')),
                ('storage', models.BooleanField(default=False, verbose_name='Storage')),
                ('co_shipping', models.NullBooleanField(verbose_name='Co-Shipping')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created on')),
                ('package_type', models.CharField(blank=True, choices=[('Food', 'Food'), ('Regular', 'Regular'), ('Luxury', 'Luxury'), ('Mix', 'Mix')], default='', max_length=16, verbose_name='Package Type')),
                ('request_ship_date', models.DateField(blank=True, null=True, verbose_name='Requested to Ship on')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Memo')),
                ('cust_tracking_num', models.CharField(blank=True, default='', max_length=32, verbose_name='Customer Tracking Number')),
                ('cust_carrier', models.CharField(blank=True, default='', max_length=32, verbose_name='Customer Carrier')),
                ('low_volume_request', models.BooleanField(default=False, verbose_name='Low Volume Request')),
                ('no_rush_request', models.BooleanField(default=False, verbose_name='No Rush Request')),
                ('wh_received_date', models.DateField(blank=True, null=True, verbose_name='Warehouse Received on')),
                ('ready_date', models.DateField(blank=True, null=True, verbose_name='Package Ready on')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Weight(kg)')),
                ('volume_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Volume Weight(kg)')),
                ('deposit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Deposit Amount')),
                ('storage_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Storage Fee')),
                ('shipping_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Shipping Fee')),
                ('currency', models.CharField(blank=True, default='', max_length=32, verbose_name='Currency')),
                ('picked_up', models.NullBooleanField(verbose_name='User Picked Up')),
                ('picked_up_date', models.DateField(blank=True, null=True, verbose_name='User Picked on')),
                ('last_shipped_date', models.DateField(blank=True, null=True, verbose_name='Last Shipped on')),
                ('tracking_num', models.CharField(blank=True, default='', max_length=20, verbose_name='Last Tracking Number')),
                ('last_carrier', models.CharField(blank=True, default='', max_length=20, verbose_name='Carrier')),
                ('status', models.CharField(blank=True, default='', max_length=20, verbose_name='Packasge Status')),
                ('issue', models.TextField(blank=True, default='', verbose_name='Package Issue')),
                ('deposit_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='deposit_payment_key', to='main.Payment', verbose_name='Deposit Confirmation')),
                ('emp_created', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_created_by_emplloyee', to='main.Employee', verbose_name='Created by Employee (order only)')),
                ('emp_pack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='package_repacked_by_employee', to='main.Employee', verbose_name='Packed by Employee')),
                ('paid_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='paid_payment_key', to='main.Payment', verbose_name='Payment Confirmation')),
                ('parent_package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.ParentPackage', verbose_name='Parent Package')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.CoReceiver', verbose_name='Receiver')),
                ('refund_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='refund_payment_key', to='main.Payment', verbose_name='Refund Confirmation')),
                ('ship_to_add', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ship_to_personal_location', to='main.Address', verbose_name='Ship to User Address')),
                ('ship_to_col', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ship_to_collection_point', to='main.CollectionPoint', verbose_name='Ship to Collection Point')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bound_email', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, default='', max_length=16, validators=[django.core.validators.RegexValidator(message="Invalid phone number format. Enter as 123-456-0987. Optionally enter extensions using 'x' followed by the number.", regex='^\\s*(?:\\+?(\\d{1,3}))?[-. (]*(\\d{3})[-. )]*(\\d{3})[-. ]*(\\d{4})(?: *x(\\d+))?\\s*$')], verbose_name='Phone Number')),
                ('reward', models.PositiveIntegerField(default=0)),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=100, verbose_name='Country')),
                ('language', models.CharField(blank=True, default='', max_length=100, verbose_name='Language')),
                ('default_address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Address', verbose_name='Default Mailing Address')),
                ('default_col', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.CollectionPoint', verbose_name='Default Collection Point')),
                ('default_pay_account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.OtherPayMethod', verbose_name='Default Payment')),
                ('default_pay_card', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Card', verbose_name='Default Payment')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=500, verbose_name='地址')),
                ('apt', models.CharField(blank=True, default='', max_length=10, verbose_name='Apartment')),
                ('city', models.CharField(default='', max_length=100, verbose_name='City')),
                ('state', models.CharField(default='', max_length=100, verbose_name='State')),
                ('country', models.CharField(default='', max_length=100, verbose_name='Country')),
                ('zipcode', models.CharField(default='', max_length=5, verbose_name='Zip Code')),
                ('name', models.CharField(default='', max_length=100, unique=True, verbose_name='Warehouse Name')),
                ('status', models.BooleanField(default=False, verbose_name='Avaliable')),
                ('memo', models.TextField(blank=True, default='', verbose_name='Memo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='service',
            name='ship_to_wh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ship_to_warehouse', to='main.Warehouse', verbose_name='Ship to Warehouse'),
        ),
        migrations.AddField(
            model_name='service',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='client_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='service',
            name='wh_received',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='received_at_warehouse', to='main.Warehouse', verbose_name='Warehouse Received'),
        ),
        migrations.AddField(
            model_name='packageimage',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Service', verbose_name='Service Key'),
        ),
        migrations.AddField(
            model_name='otherpaymethod',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Payment Id'),
        ),
        migrations.AddField(
            model_name='item',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Service', verbose_name='Service Key'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='coreceiver',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Payment Id'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='coreceiver',
            unique_together={('user', 'first_name', 'last_name', 'phone')},
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('user', 'first_name', 'last_name', 'phone', 'email', 'address', 'apt', 'city', 'state', 'country', 'zipcode')},
        ),
    ]
