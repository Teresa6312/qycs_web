from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.validators import RegexValidator
from django.urls import reverse

phone_regex = RegexValidator(regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', \
	message="Invalid phone number format. Enter as 123-456-0987. Optionally enter extensions using 'x' followed by the number.")


class Location(models.Model):
	id=models.PositiveIntegerField(primary_key=True)
	city=models.CharField(max_length=100, blank = True, default = '')
	state=models.CharField(max_length=100, blank = True, default = '')
	country=models.CharField(max_length=100, blank = True, default = '')
	country_sortname=models.CharField(max_length=100, blank = True, default = '')


# from django.contrib.auth import get_user_model
# UserModel = get_user_model()
# to set email is required

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key = True)
	position = models.CharField(max_length=100, blank = True, default = '')

	def __str__(self):
		return '%s %s: %s'%(self.user.first_name, self.user.last_name, self.position)



class Address_Common_Info(models.Model):
	address = models.CharField(max_length=500, default='',verbose_name='地址' )
	apt = models.CharField(blank=True, max_length=10, default='',verbose_name='Apartment' )
	city = models.CharField(max_length=100, default='',verbose_name= 'City')
	state = models.CharField(max_length=100, default='',verbose_name= 'State')
	country = models.CharField(max_length=100, default='',verbose_name= 'Country')
	zipcode = models.CharField(max_length=5, default='', verbose_name= 'Zip Code')
	memo = models.TextField(blank = True, default='', verbose_name= 'Address Meno')

	class Meta:
		abstract = True



class Address(Address_Common_Info):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name= 'User')
	#when the user delete or unsave the address set it as null


	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True,default='',verbose_name= 'First Name')
	last_name = models.CharField(max_length=100, blank=True,default='',verbose_name= 'Last Name')
	phone = models.CharField(validators=[phone_regex], max_length=16, blank=True, default='',verbose_name= 'Phone Number')
	email = models.EmailField(max_length=100, blank=True, default='',verbose_name= 'Email Address')
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True)
	def __str__(self):
		return '%s %s\n %s %s, %s %s'%(self.first_name, self.last_name, self.address, self.city, self.state, self.zipcode)

	def get_absolute_url(self):

	    return dict(edit=reverse('editaddress', args=[str(self.id)]),
					delete=reverse('deleteaddress', args=[str(self.id)]),
					set_default=reverse('set_dedault_address', args=[str(self.id)])
					)

	class Meta:
		unique_together=('user'
		,'first_name'
		,'last_name'
		,'phone'
		,'email'
		,'address'
		,'apt'
		,'city'
		,'state'
		,'country'
		,'zipcode'
		)

# from django.db import models
# from django_google_maps import fields as map_fields
#
# class Rental(models.Model):
# 	address = map_fields.AddressField(max_length=200)
# 	geolocation = map_fields.GeoLocationField(max_length=100)


class Card(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL, blank=True, null=True,
		verbose_name= 'Payment Id'
	)
	address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=False, default = '', verbose_name= 'Address')
	card_num = models.CharField(max_length = 16, unique = True, default='',verbose_name= 'Card Number')
	card_exp = models.CharField(max_length = 6, default='',verbose_name= 'Expiration Date(MM/YY)')
	card_security_code = models.CharField(max_length = 6, default='',verbose_name= 'Security Code')

	def __str__(self):
		if self.pay_method.user.last_name == self.address.last_name and self.pay_method.user.first_name == self.address.first_name:
			return '%s : %s'%(self.pay_method, self.card_num)
		else:
			return '%s %s (%s: %s)'%(self.pay_method, self.address.first_name, self.address.last_name, self.card_num)


class OtherPayMethod(models.Model):
	METHOD_CHOICE = (
		('Alipay', 'Alipay'),
		('Paypal', 'Paypal'),
		('WeChat', 'WeChat'),
	)
	user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL, blank=True, null=True,
		verbose_name= 'Payment Id'
	)
	method = models.CharField( max_length = 10, choices = METHOD_CHOICE, verbose_name= 'Method')
	email = models.EmailField(max_length = 100, blank=True, default='',verbose_name= 'Email Address')
	phone = models.CharField(validators=[phone_regex], max_length=16, blank=True, default='',verbose_name= 'Phone Number')
	account_id = models.CharField(max_length = 64, blank=True, default='',verbose_name= 'Account Id')
	account_name = models.CharField(max_length = 64, blank=True, default='',verbose_name= 'Account Name')

	def __str__(self):
		if self.account_name != '' and self.account_name != None:
			name = self.account_name
		elif self.email != '' and self.email != None:
			name = self.email
		elif self.account_id != '' and self.account_id != None:
			name = self.account_id
		else:
			name = self.phone
		return '%s %s'%(self.pay_method,name)
	class Meta:
		verbose_name_plural = "Other Pay Method"


class CollectionPoint(Address_Common_Info):
	collector = models.OneToOneField(
		User,
		on_delete=models.PROTECT,
		primary_key=True,
		verbose_name= 'Collector'
	)
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
	name = models.CharField(max_length = 16, unique = True, default='', verbose_name= 'Collection Point Name')
	license = models.CharField(max_length = 32, default='',verbose_name= 'License Number')
	license_type = models.CharField(max_length = 32, default='',verbose_name= 'License Type')
	license_image = models.ImageField(upload_to = 'collector_license', blank = 'True')
	id_image = models.ImageField(upload_to = 'collector_id', default = '')
	store_name = models.CharField(max_length = 16, unique = True, default='', verbose_name= 'Store Name')
	store = models.BooleanField(default = True, verbose_name= 'Store')
	store.boolean = True
	status = models.BooleanField(default = False, verbose_name= 'Avaliable')
	status.boolean = True
	location_image = models.ImageField(upload_to = 'collector_image', blank ='True')
	longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
	dimension = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
	food = models.BooleanField(default = False)
	regular = models.BooleanField(default = False)
	luxury = models.BooleanField(default = False)



	def __str__(self):
		return '%s %s %s'%(self.name, self.collector.first_name, self.collector.last_name)

	def get_absolute_url(self):
		return dict(collection_point_view=reverse('collection_point_view', args=[str(self.pk)]),
					add_co_shipping=reverse('add_co_shipping', args=[str(self.pk)])
					)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key = True)
	bound_email = models.BooleanField(default =False)
	bound_email.boolean = True
	phone = models.CharField(validators=[phone_regex], max_length=16, blank=True, default='',verbose_name= 'Phone Number')
	default_address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True, verbose_name= 'Default Mailing Address')
	default_col = models.ForeignKey(CollectionPoint, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name= 'Default Collection Point')

	reward = models.PositiveIntegerField(default = 0)
	birthday = models.DateField(blank=True, null=True,verbose_name= 'Date of Birth')
	default_pay_card = models.OneToOneField(Card, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name= 'Default Payment')
	default_pay_account = models.OneToOneField(OtherPayMethod, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name= 'Default Payment')
	updated_date = models.DateTimeField(auto_now = True, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, default='',verbose_name= 'Country')
	language = models.CharField(max_length=100, blank=True, default='',verbose_name= 'Language')

	def __str__(self):
		return '%s %s'%(self.user.first_name, self.user.last_name)

def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender = User)



class CoReceiver(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
	first_name = models.CharField(max_length = 100, blank=True, default='', verbose_name= 'First Name')
	last_name = models.CharField(max_length = 100, blank=True, default='', verbose_name= 'Last Point Name')
	phone = models.CharField(validators=[phone_regex], max_length=25, blank=True, default='',verbose_name= 'Phone Number')

	def __str__(self):
		if self.user != None:
			return '%s %s'%(self.user.first_name, self.user.last_name)
		else:
			return '%s %s'%(self.first_name, self.last_name)

	class Meta:
		unique_together=('user','first_name','last_name','phone')


def create_coreceiver(sender, **kwargs):
	if kwargs['created']:
		co_receiver = CoReceiver.objects.create(user = kwargs['instance'])

post_save.connect(create_coreceiver, sender = User)







class Warehouse(Address_Common_Info):
	name = models.CharField(max_length=100, unique=True, default='',verbose_name= 'Warehouse Name')
	status = models.BooleanField(default = False,verbose_name= 'Avaliable')
	status.boolean = True
	memo = models.TextField(blank=True, default='',verbose_name= 'Memo')
	status.boolean = True

	def __str__(self):
		return '%s - %s'%(self.country, self.name)





# !!!!!!!!!!! encryption required !!!!!!!!!!!!


class Coupon(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, blank = True, null=True, verbose_name= 'User')
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
	code = models.CharField(max_length = 16, unique = True, default='',verbose_name= 'Coupon Code')
	discount = models.PositiveIntegerField(default = 5, verbose_name = 'Discount')
	amount_limit = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Amount Limit')
	start_date = models.DateTimeField(blank = True, null = True, verbose_name= 'Start on')
	end_date = models.DateTimeField(blank = True, null = True, verbose_name= 'End on')

	package = models.BooleanField(default = False, verbose_name= 'Good For Package')
	package.boolean = True

	order = models.BooleanField(default = False,verbose_name= 'Good For Order')
	order.boolean = True

	one_time_only = models. BooleanField(default = True, verbose_name= 'One Time Use Only')
	used_times = models. PositiveIntegerField(default=0,verbose_name= 'Coupon Used Times')
	memo = models.TextField(blank=True, default='',verbose_name= 'Memo')

	def __str__(self):
		return '%s %d %s'%(self.code,self.discount,"% OFF")

class Payment(models.Model):
	pay_by_card = models.ForeignKey(Card, on_delete=models.PROTECT, default = '', verbose_name= 'Card Payment Id')
	pay_by_other = models.ForeignKey(OtherPayMethod, on_delete=models.PROTECT, verbose_name= 'Other Payment Id')
	pay_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= 'Pay on')
	transaction_id = models.CharField(max_length = 32, blank = False, default='',verbose_name= 'Payment Confirmation',unique = True)# would the different method  have the same transaction id?
	coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, blank= True, null=True,verbose_name= 'Coupon')
	deposit = models.BooleanField(default=False,verbose_name= 'Deposit')
	deposit.boolean = True

	amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name= 'Paid Amount')
	currency= models.CharField(max_length = 32, default='',verbose_name= 'Currency')
	memo = models.TextField(blank=True, default='',verbose_name= 'Memo')

	def __str__(self):
		return '%s %f %s'%(self.pay_method, self.amount, self.currency)



class ParentPackage(models.Model):

	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= 'Created on')
	emp_pack = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank = True, null=True, related_name='package_pack_by_employee',verbose_name= 'Packed by Employee')
	packed_date = models.DateField(blank=True, null=True,verbose_name= 'Packed on')
	memo = models.TextField(blank=True, default='',verbose_name= 'Memo')
	weight = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= 'Weight(kg)')

	tracking_num = models.CharField(max_length=32, blank=True, default='',verbose_name= 'Tracking Number')
	carrier = models.CharField(max_length=32, blank=True, default='',verbose_name= 'Carrier')
	shipped_date = models.DateField(blank=True, null=True,verbose_name= 'Shipped on')
	received_date = models.DateField(blank=True, null=True,verbose_name= 'Received on')
	emp_split = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank = True, null=True, related_name='emplloyee_splited_package',verbose_name= 'Splitted by Employee')

	status = models.CharField(max_length=100, blank=True, default='',verbose_name= 'Status')
	issue = models.TextField(blank=True, default='',verbose_name= 'Accident Memo')

	def __str__(self):
		return self.tracking_num



class Service(models.Model):
	TYPE_CHOICE = (
		('Food', 'Food'),
		('Regular', 'Regular'),
		('Luxury', 'Luxury'),
		('Mix', 'Mix'),
	)

	user = models.ForeignKey(User, on_delete=models.DO_NOTHING , related_name='client_user',verbose_name= 'User')

	order = models.BooleanField(default=False,verbose_name= 'Order')
	storage = models.BooleanField(default=False,verbose_name= 'Storage')
	co_shipping = models.NullBooleanField(verbose_name= 'Co-Shipping')
	parent_package = models.ForeignKey(ParentPackage, on_delete=models.DO_NOTHING, blank = True, null=True,verbose_name= 'Parent Package')
	created_date = models.DateTimeField(auto_now_add = True, blank=True, null=True, verbose_name= 'Created on')
	package_type = models.CharField(max_length = 16, choices = TYPE_CHOICE, blank=True, default='',verbose_name = 'Package Type')  # create a choice?

	emp_created = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank = True, null=True, related_name='order_created_by_emplloyee',verbose_name= 'Created by Employee (order only)') # for order only
	request_ship_date = models.DateField(blank=True, null=True, verbose_name= 'Requested to Ship on')
	memo = models.TextField(blank=True, default='',verbose_name= 'Memo')
	cust_tracking_num = models.CharField(max_length = 32, blank=True, default='',verbose_name= 'Customer Tracking Number')
	cust_carrier = models.CharField(max_length = 32, blank=True, default='',verbose_name= 'Customer Carrier')# need to set up choice
	low_volume_request = models.BooleanField(default = False,verbose_name= 'Low Volume Request')
	no_rush_request = models.BooleanField(default = False,verbose_name= 'No Rush Request')

	wh_received = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, null=True, related_name='received_at_warehouse',verbose_name= 'Warehouse Received')
	wh_received_date = models.DateField(blank=True, null=True,verbose_name= 'Warehouse Received on')
	ready_date = models.DateField(blank=True, null=True, verbose_name= 'Package Ready on')
	emp_pack = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,  blank = True, null=True, related_name='package_repacked_by_employee', verbose_name= 'Packed by Employee')
	weight = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= 'Weight(kg)')
	volume_weight = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= 'Volume Weight(kg)')
	deposit = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2 , verbose_name= 'Deposit Amount')
	deposit_key = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='deposit_payment_key', verbose_name= 'Deposit Confirmation')

	storage_fee = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= 'Storage Fee')
	shipping_fee = models.DecimalField( blank=True, null=True, max_digits=10, decimal_places=2, verbose_name= 'Shipping Fee')
	currency = models.CharField(max_length = 32, blank=True, default='', verbose_name= 'Currency') # need to set up choice
	paid_key = models.ForeignKey(Payment, on_delete=models.DO_NOTHING,  blank=True, null=True, related_name='paid_payment_key', verbose_name= 'Payment Confirmation')


	ship_to_add = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ship_to_personal_location', verbose_name= 'Ship to User Address')

	ship_to_col = models.ForeignKey(CollectionPoint, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ship_to_collection_point', verbose_name= 'Ship to Collection Point')
	receiver = models.ForeignKey(CoReceiver, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name= 'Receiver')

	ship_to_wh = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ship_to_warehouse', verbose_name= 'Ship to Warehouse')

	picked_up = models.NullBooleanField(verbose_name= 'User Picked Up')
	picked_up_date = models.DateField(blank=True, null=True, verbose_name= 'User Picked on')

	last_shipped_date = models.DateField(blank=True, null=True, verbose_name= 'Last Shipped on')
	tracking_num = models.CharField(max_length = 20, blank=True, default='', verbose_name= 'Last Tracking Number')
	last_carrier = models.CharField(max_length = 20, blank=True, default='', verbose_name= 'Carrier')# need to set up choice

	status = models.CharField(max_length = 20, blank=True, default='', verbose_name= 'Packasge Status')
	issue = models.TextField(blank=True, default='', verbose_name= 'Package Issue')
	refund_key = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='refund_payment_key', verbose_name = 'Refund Confirmation')


	def __str__(self):
		if self.ship_to_col != '' and self.ship_to_col != None:
			ship_to = self.ship_to_col
		elif self.ship_to_add != '' and self.ship_to_add != None:
			ship_to = self.ship_to_add
		else:
			ship_to = self.ship_to_wh

		if self.order:
			return "%s's Order created on %s \n ship to %s"%(self.user, self.created_date, ship_to)
		elif self.co_shipping:
			return "%s's package created on %s \n ship to %s"%(self.user, self.created_date, ship_to)
		else:
			return "%s's package created on %s \n"%(self.user, self.created_date)

	def get_absolute_url(self):
		return reverse('package_detail', args=[str(self.id)])

class Item(models.Model):
	service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, verbose_name = 'Service Key')
	item_name = models.CharField(max_length = 100, blank=False, default='', verbose_name = 'Item Name')
	item_detail = models.CharField(max_length = 100, blank=True, default='', verbose_name = 'Item Details')
	item_quantity = models.PositiveIntegerField(blank=False, default=1, verbose_name = 'quantity')
	item_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default= 0.0, verbose_name = 'Item Value')
	currency = models.CharField(max_length = 16, blank=True, default='', verbose_name = 'Currency')
	tax_included = models.BooleanField(default=True, verbose_name = 'Included Tax')# for order only
	order_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, blank = True, null=True, verbose_name = 'Order by Employee')# for order only
	item_url  = models.CharField(max_length = 1000, blank=True, default='', verbose_name = 'Item URL')
	memo = models.TextField(blank=True, default='', verbose_name = 'Memo')
	low_volume_request = models.BooleanField(default = True,verbose_name= 'Low Volume Request')
	issue = models.TextField(blank=True, default='', verbose_name = 'Item Issue')

	def __str__(self):
		return self.item_name


#
# set up the upload path
class PackageImage(models.Model):
	package = models.ForeignKey(Service, on_delete=models.DO_NOTHING, verbose_name = 'Service Key')
	image = models.ImageField(upload_to = 'package_snapshot')


class FavoriteWebsite(models.Model):
	TYPE_CHOICE = (
		('Clothing', 'Clothing'),
		('Bag', 'Bag'),
		('Jewelry', 'Jewelry'),
		('Sport', 'Sport'),
		('Beauty', 'Beauty'),
		('Baby', 'Baby'),
		('Other', 'Other'),
	)
	country = models.CharField(max_length=100, blank=True, default='',verbose_name= 'Country')
	web_type = models.CharField(max_length = 32, choices = TYPE_CHOICE, blank=True, default='',verbose_name = 'Websit Type')
	web_name = models.CharField(max_length = 64, blank=True, default='', verbose_name = 'Websit Name')
	web_url = models.URLField (max_length = 128, blank=True, default='', verbose_name = 'Websit url')
	rate = models.PositiveIntegerField(default=1, verbose_name = 'Rate')
