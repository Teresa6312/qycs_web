from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *
from django.utils.html import mark_safe



admin.site.unregister(User)

class EmployeeInline(admin.StackedInline):
	model = Employee
	can_delete = False
	verbose_name_plural = 'employee'

class AddressInline(admin.StackedInline):
	model = Address
	extra = 1
	can_delete = False
	fields = ['first_name', 'last_name','email', 'phone', 'address', 'city', 'state','country', 'zipcode','memo', ]
	verbose_name_plural = 'address list'

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'other information'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
	inlines = (EmployeeInline, UserProfileInline, AddressInline, )
	search_fields = ['username', 'first_name', 'last_name']



# Re-register UserAdmin
admin.site.register(User, UserAdmin,)






class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('pk', 'user', 'bound_email', 'phone', 'country', 'reward', )
	list_filter = ['country']


admin.site.register(UserProfile, UserProfileAdmin)






class AddressAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'first_name', 'last_name', 'address','apt',  'city', 'state','country', 'zipcode')
	list_filter = ['country', 'state','city']
	search_fields = ['first_name', 'last_name', ]

	fieldsets = [
		('User', 				{'fields': ['user',]}),
		('Address',               {'fields': ['first_name', 'last_name','email', 'phone', 'address', 'city', 'state','country', 'zipcode','memo']}),
	]

admin.site.register(Address, AddressAdmin,)





class CoReceiverAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'first_name', 'last_name', 'phone')
	search_fields = ['first_name', 'last_name','phone']


admin.site.register(CoReceiver, CoReceiverAdmin)






class CollectionPointAdmin(admin.ModelAdmin):
	list_display = ('collector', 'name', 'store_name', 'address', 'city', 'state','country', 'zipcode', 'status')
	list_filter = ['country', 'state','city', 'status', 'store']
	search_fields = ['name']
	readonly_fields = [ "collector_image"]

	def collector_image(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url = obj.location_image.url,
			width=obj.location_image.width,
			height=obj.location_image.height,
			)
		)

	fieldsets = [
		('Collector', 				{'fields': ['collector', 'store', 'status']}),
		('Address',               	{'fields': ['address', 'city', 'state','country', 'zipcode','memo','name']}),
		('License',					{'fields': ['license', 'license_type']}),
		('Image',					{'fields': ['location_image', 'collector_image']}),
	]


admin.site.register(CollectionPoint, CollectionPointAdmin)






class CouponAdmin(admin.ModelAdmin):
	list_display = ('code','discount', 'user', 'package','order', 'one_time_only', 'used_times')
	list_filter = ['package', 'order', 'one_time_only']
	search_fields = ['code']
	# how to add search for user

	fieldsets = [
		('Coupon', 				{'fields': ['code', 'discount', 'start_date', 'end_date', 'memo']}),
		('Limits',               	{'fields': ['user', 'one_time_only', 'package','order']}),
	]

admin.site.register(Coupon, CouponAdmin,)





class ServiceInline(admin.TabularInline):
	model = Service
	fields = ('id', 'user', 'receiver',)
	verbose_name_plural = "Packages/Orders"
	extra = 1

class ParentPackageAdmin(admin.ModelAdmin):
	inlines = (ServiceInline,)
	list_display = ('created_date','packed_date', 'shipped_date', 'tracking_num')
	list_filter = ['created_date', 'packed_date', 'shipped_date']
	fieldsets = [
		('Creation', 				{'fields': [ 'packed_date', 'emp_pack', 'weight', 'memo']}),
		('Shipment',               	{'fields': ['shipped_date', 'tracking_num', 'carrier','received_date', 'status']}),  # how to add the ship to infor from service
		('Shipped to Warehouse',    {'fields': ['emp_split'], 'classes': ['collapse']}),
		('Accident', {'fields': ['issue']}),
	]

# How to add the service fields here
admin.site.register(ParentPackage, ParentPackageAdmin,)





admin.site.register(Card)

admin.site.register(OtherPayMethod)





class WarehouseAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'city', 'state','country', 'zipcode', 'status')
	search_fields = ['name']
	list_filter = ['country', 'state','city']


	fieldsets = [
		('Name', 				{'fields': ['name', 'status']}),
		('Address',               {'fields': ['address', 'city', 'state','country', 'zipcode']}),
		('Memo', {'fields': ['memo']}),
	]



admin.site.register(Warehouse, WarehouseAdmin,)



class ItemInline(admin.StackedInline):
	model = Item
	extra = 1




class PackageImageInline(admin.StackedInline):
	model = PackageImage
	extra = 1
	readonly_fields = [ "package_image"]
	fields = ('image', 'package_image', )

	def package_image(self, obj):
		return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
			url = obj.image.url,
			width=obj.image.width,
			height=obj.image.height,
			)
		)


class ServiceAdmin(admin.ModelAdmin):


	# Check this if it can fix the search for user issue
	# def get_queryset(self, request):
	# 	queryset = super().get_queryset(request)
	# 	queryset = queryset.annotate(
	# 	_hero_count=Count("hero", distinct=True),
	# 	_villain_count=Count("villain", distinct=True),
	# 	)
	# 	return queryset


	inlines = (ItemInline, PackageImageInline, )
	list_display = ('user', 'storage', 'order', 'co_shipping','cust_tracking_num', 'wh_received', 'created_date','status')
	search_fields = ['cust_tracking_num']
	list_filter = ['storage', 'order','co_shipping', 'wh_received']

	fieldsets = [
		('Order or Customer package', 		{'fields': ['order', 'emp_created']}),
		('To storage',               		{'fields': ['storage', 'request_ship_date'], 'classes': ['collapse']}),
		('Shipping Type', 					{'fields': ['co_shipping']}),
		('Creation', 						{'fields': [ 'user', 'cust_tracking_num','cust_carrier', 'low_volume_request', 'no_rush_request', 'memo']}),
		('Service Started at Warehouse', 	{'fields': ['wh_received', 'wh_received_date', 'emp_pack', 'weight', 'ready_date']}),
		('Deposit', 						{'fields': ['deposit'], 'classes': ['collapse']}),
		('Charges', 						{'fields': ['storage_fee', 'shipping_fee', 'currency']}),
		('Shipment', 						{'fields': ['ship_to_add', 'ship_to_col', 'ship_to_wh', 'last_shipped_date', 'tracking_num', 'last_carrier']}),
		('Receiver', 						{'fields': ['receiver', 'picked_up', 'picked_up_date']}),
		('Issue', 							{'fields': ['issue'], 'classes': ['collapse']})

	]

	# how to search user!!!!!!!!!!!!
admin.site.register(Service, ServiceAdmin, )


class PackageImageAdmin(admin.ModelAdmin):
	list_display = ('package', 'image')
	search_fields = ['package']

admin.site.register(PackageImage, PackageImageAdmin, )



class FavoriteWebsiteAdmin(admin.ModelAdmin):
	list_display = ('web_name', 'web_type', 'country', 'rate')
	search_fields = ['web_name']

admin.site.register(FavoriteWebsite, FavoriteWebsiteAdmin)




from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class RentalAdmin(admin.ModelAdmin):
	formfield_overrides = {
		map_fields.AddressField: {
			'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})
		},
		# map_fields.GeoLocationField: {
		# 	'widget': map_widgets.GoogleMapsGeoLocationWidget
		# },
	}
# 	- To change the map type (`hybrid` by default), you can add an html attribute
# on the `AddressField` widget. The list of allowed values is: `hybrid`, `roadmap`, `satellite`, `terrain`
