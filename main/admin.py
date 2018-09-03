from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import NewUserCreationForm, NewUserChangeForm
from .models import (
	User, Employee, Address, CollectionPoint, Service,
	Warehouse, PackageSnapshot, ParentPackage, Item, Payment,
	Coupon, FavoriteWebsite, Resource
)
from django.utils.html import mark_safe



# admin.site.unregister(User)


class EmployeeInline(admin.StackedInline):
	model = Employee
	can_delete = False

class AddressInline(admin.StackedInline):
	model = Address
	can_delete = False
	extra = 1
	can_delete = False
	fields = ['first_name', 'last_name', 'phone', 'address', 'city', 'state','country', 'zipcode','memo', ]
	verbose_name_plural = 'address list'


# Define a new User admin
class NewUserAdmin(UserAdmin):
	model = User
	add_form = NewUserCreationForm
	form = NewUserChangeForm

	inlines = (EmployeeInline, AddressInline, )
	list_filter = ['country']
	list_display = ['username', 'first_name', 'last_name','email','email_confirmed', 'phone', 'country', 'reward']
	search_fields = ['username','first_name', 'last_name', 'email', 'phone']

	fieldsets = [
		(None, 		{'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'country', 'language', 'default_address', 'default_col', 'reward',)}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	]


admin.site.register(User, NewUserAdmin)


class PaymentAdmin(admin.ModelAdmin):
	list_display = ['transaction_id', 'pay_date', 'coupon','deposit','amount', 'currency',]

admin.site.register(Payment, PaymentAdmin)



class AddressAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'first_name', 'last_name', 'address','apt',  'city', 'state','country', 'zipcode')
	list_filter = ['country', 'state','city']
	search_fields = ['first_name', 'last_name', ]

	fieldsets = [
		('User', 				{'fields': ['user',]}),
		('Address',             {'fields': ['first_name', 'last_name', 'phone', 'address', 'city', 'state','country', 'zipcode']}),
		('Memo', 				{'fields': ['memo',]}),
	]

admin.site.register(Address, AddressAdmin,)




class CollectionPointAdmin(admin.ModelAdmin):
	list_display = ('collector', 'name', 'address', 'city', 'state','country', 'zipcode', "status", 'absent_start', 'absent_end')
	list_filter = ['country', 'state','city', "status", 'store']
	search_fields = ['name']
	readonly_fields = [ "collector_icon_display", "license_image_display", "id_image_display", "status_all_display"]

	def collector_icon_display(self, obj):
		return mark_safe('<img src="{url}" width="500px"/>'.format(
			url = obj.collector_icon.url,
			width=obj.collector_icon.width,
			height=obj.collector_icon.height,
			)
		)
	def license_image_display(self, obj):
		return mark_safe('<img src="{url}" width="500px"/>'.format(
			url = obj.license_image.url,
			width=obj.license_image.width,
			height=obj.license_image.height,
			)
		)
	def id_image_display(self, obj):
		return mark_safe('<img src="{url}" width="500px"/>'.format(
			url = obj.id_image.url,
			width=obj.id_image.width,
			height=obj.id_image.height,
			)
		)
	def status_all_display(self, obj):
		return obj.status_all()

	fieldsets = [
		('Collector', 				{'fields': ['collector', 'store', 'status',"status_all_display",]}),
		('location',               	{'fields': ['name','collector_icon', 'collector_icon_display', 'store', 'store_name', 'address', 'city', 'state','country', 'zipcode','memo',]}),
		('License',					{'fields': ['license_image', 'license_image_display', 'id_image','id_image_display',]}),
		('Document',				{'fields': ['wechat', 'wechat_qrcode', 'referrer', 'apply_reason', 'info_source',]}),
		('Package',                 {'fields': ['food', 'regular', 'skincare',]}),
		('Schedule',                {'fields': ['absent_start', 'absent_end',
												'mon_start', 'mon_end',
												'tue_start', 'tue_end',
												'wed_start', 'wed_end',
												'thu_start', 'thu_end',
												'fri_start', 'fri_end',
												'sat_start', 'sat_end',
												'sun_start', 'sun_end',]}),
	]


admin.site.register(CollectionPoint, CollectionPointAdmin)





# how to add search for user
class CouponAdmin(admin.ModelAdmin):
	list_display = ('code','discount', 'user', 'package','order', 'one_time_only', 'used_times')
	list_filter = ['package', 'order', 'one_time_only']
	search_fields = ['code']


	fieldsets = [
		('Coupon', 				{'fields': ['code', 'discount', 'start_date', 'end_date', 'memo']}),
		('Limits',               	{'fields': ['user', 'one_time_only', 'package','order']}),
	]

admin.site.register(Coupon, CouponAdmin,)





class ServiceInline(admin.TabularInline):
	model = Service
	fields = ('id', 'user', 'receiver', 'ship_to_add', 'ship_to_col')
	can_delete = False

class ParentPackageAdmin(admin.ModelAdmin):
	inlines = (ServiceInline,)
	list_display = ('created_date','packed_date', 'shipped_date', 'tracking_num')
	list_filter = ['created_date', 'packed_date', 'shipped_date']
	readonly_fields = [ "ship_to", ]

	def ship_to(self, obj):
		if obj.sevice_set.first().ship_to_add:
			return obj.sevice_set.first().ship_to_add
		elif obj.sevice_set.first().ship_to_col:
			return obj.sevice_set.first().ship_to_col
		elif obj.sevice_set.first().ship_to_wh:
			return obj.sevice_set.first().ship_to_wh
		else:
			return None


	fieldsets = [
		('Creation', 				{'fields': [ 'packed_date', 'emp_pack', 'weight', 'memo']}),
		('Shipment',               	{'fields': ['ship_to', 'shipped_date', 'tracking_num', 'carrier','received_date']}),
		('Shipped to Warehouse from Warehouse',    {'fields': ['emp_split'], 'classes': ['collapse']}),
		('Issue',                   {'fields': ['issue']}),
	]


admin.site.register(ParentPackage, ParentPackageAdmin,)



class WarehouseAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'city', 'state','country', 'zipcode', 'status')
	search_fields = ['name']
	list_filter = ['country', 'state','city']


	fieldsets = [
		('Name', 				  {'fields': ['name', 'status']}),
		('Address',               {'fields': ['address', 'city', 'state','country', 'zipcode']}),
		('Memo',                  {'fields': ['memo']}),
	]



admin.site.register(Warehouse, WarehouseAdmin,)



class ItemInline(admin.StackedInline):
	model = Item
	can_delete = False


class PackageSnapshotInline(admin.StackedInline):
	model = PackageSnapshot
	extra = 1
	readonly_fields = [ "snapshot_display"]
	fields = ('snapshot','snapshot_display', )
	can_delete = False

	def snapshot_display(self, obj):
		return mark_safe('<img src="{url}" width="500px" />'.format(
			url = obj.snapshot.url,
			width=obj.snapshot.width,
			height=obj.snapshot.height,
			)
		)



class ServiceAdmin(admin.ModelAdmin):
	inlines = (ItemInline, PackageSnapshotInline, )
	list_display = ('user', 'storage', 'order', 'co_shipping','cust_tracking_num', 'wh_received', 'created_date')
	search_fields = ['cust_tracking_num']
	list_filter = ['storage', 'order','co_shipping', 'wh_received']
	readonly_fields = [ "status_all_display"]

	def status_all_display(self, obj):
		return obj.status_all()

	fieldsets = [
		('Order or Customer package', 		{'fields': ['order', 'emp_created']}),
		('To storage',               		{'fields': ['storage', 'request_ship_date'], 'classes': ['collapse']}),
		('Shipping Type', 					{'fields': ['co_shipping']}),
		('Creation', 						{'fields': [ 'user', 'cust_tracking_num','cust_carrier', 'low_volume_request', 'no_rush_request', 'memo']}),
		('Status', 							{'fields': ['status_all_display']}),
		('Service Started at Warehouse', 	{'fields': ['wh_received', 'wh_received_date', 'emp_pack', 'weight', 'ready_date']}),
		('Deposit', 						{'fields': ['deposit'], 'classes': ['collapse']}),
		('Charges', 						{'fields': ['storage_fee', 'shipping_fee', 'currency']}),
		('Shipment', 						{'fields': ['ship_to_add', 'ship_to_col', 'ship_to_wh', 'last_shipped_date', 'tracking_num', 'last_carrier']}),
		('Receiver', 						{'fields': ['receiver', 'picked_up', 'picked_up_date']}),
		('Issue', 							{'fields': ['issue'], 'classes': ['collapse']})

	]

admin.site.register(Service, ServiceAdmin, )




class FavoriteWebsiteAdmin(admin.ModelAdmin):
	list_display = ('web_name', 'web_type', 'country', 'rate')
	search_fields = ['web_name']

admin.site.register(FavoriteWebsite, FavoriteWebsiteAdmin)

class ResourceAdmin(admin.ModelAdmin):
	list_display = ('id', 'title','header',)
	search_fields = ['title', 'header',]

admin.site.register(Resource, ResourceAdmin)
