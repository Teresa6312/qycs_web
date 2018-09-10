from django import forms
from .models import (
	User, Address, Service, CollectionPoint, Warehouse,
	Item, PackageSnapshot, CoReceiver, FavoriteWebsite,
	CARRIER_CHOICE, phone_regex, OrderSet
	)
# from django.core.exceptions import ObjectDoesNotExist, NON_FIELD_ERRORS
#used to catch errors related to populating the form fields from a related Project

from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

import datetime

year = datetime.datetime.now().year
birthday_years = [i for i in range(year-100,year)]
schedule_years = [year, year+1]

class NewUserCreationForm(UserCreationForm):
	birthday = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = birthday_years))
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username', 'email', 'first_name', 'last_name',
					'phone', 'country', 'language', 'birthday', 'password1', 'password2',)

	def save(self, commit=True, *args, **kwargs):
		user = super(NewUserCreationForm, self).save(commit=False, *args, **kwargs)
		user.first_name = user.first_name.title()
		user.last_name = user.last_name.title()
		user.email = user.email.lower()
		user.country = user.country.upper()
		if commit:
			user.save()
		return user

class NewUserChangeForm(UserChangeForm):
	birthday = forms.DateField(required = False, widget=forms.SelectDateWidget(
				empty_label=("Year", "Month", "Day"),
				years = birthday_years))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name',
					'phone', 'country', 'language', 'birthday',
					'default_address', 'default_col', 'password',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance:
			try:
				user = User.objects.get(id = self.instance.id)
				if user.collectionpoint:
					self.fields['first_name'].widget.attrs['readonly'] = True
					self.fields['last_name'].widget.attrs['readonly'] = True
					self.fields['email'].widget.attrs['readonly'] = True
				elif user.email_confirmed:
					self.fields['email'].widget.attrs['readonly'] = True
				if user.birthday:
					self.fields['birthday'].widget.attrs['readonly'] = True
			except:
				pass

	def save(self, commit=True, *args, **kwargs):
		user = super(NewUserChangeForm, self).save(commit=False, *args, **kwargs)
		user.first_name = user.first_name.title()
		user.last_name = user.last_name.title()
		user.email = user.email.lower()
		user.country = user.country.upper()
		if commit:
			user.save()
		return user

class FavoriteWebsiteForm(forms.ModelForm):

	class Meta:
		model = FavoriteWebsite
		fields = ('web_type', 'web_name',)

WebFormSet = formset_factory(FavoriteWebsiteForm, extra = 3, max_num = 3)


#-----------------------------------------------------------------------------------------
'''
Create new Address
'''
#-----------------------------------------------------------------------------------------
class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		exclude = ('meno',)

	def save(self, commit=True, *args, **kwargs):
		add = super(AddressForm, self).save(commit=False, *args, **kwargs)
		add.first_name = add.first_name.title()
		add.last_name = add.last_name.title()
		add.address = add.address.title()
		add.apt = add.apt.title()
		add.city = add.city.title()
		add.state = add.state.title()
		add.country = add.country.upper()
		if commit:
			add.save()
		return add

class ColCreationForm(forms.ModelForm):
	agreement = forms.BooleanField(required = True, label = _("Agree"))
	class Meta:
		model = CollectionPoint
		fields = ('store','store_name','license_type', 'license_image','id_image',
					'address','apt','city','state','country','zipcode',
					'collector_icon', 'name', 'wechat', 'wechat_qrcode',
					'referrer', 'apply_reason', 'info_source','agreement')

class ColChangeForm(forms.ModelForm):
	absent_start = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = schedule_years))
	absent_end = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = schedule_years))
	# forms.ChoiceField(label = _("Carrier")
	# mon_start = forms.TimeField(required = False)
	# mon_end = forms.TimeField(required = False)
	# tue_start = forms.TimeField(required = False)
	# tue_end = forms.TimeField(required = False)
	# wed_start = forms.TimeField(required = False)
	# wed_end = forms.TimeField(required = False)
	# thu_start = forms.TimeField(required = False)
	# thu_end = forms.TimeField(required = False)
	# fri_start = forms.TimeField(required = False)
	# fri_end = forms.TimeField(required = False)
	# sat_start = forms.TimeField(required = False)
	# sat_end = forms.TimeField(required = False)
	# sun_end = forms.TimeField(required = False)

	class Meta:
		model = CollectionPoint
		fields = ('collector_icon', 'wechat', 'wechat_qrcode','description',
					'mon_start', 'mon_end', 'tue_start', 'tue_end',
					'wed_start','wed_end','thu_start','thu_end',
					'fri_start','fri_end','sat_start','sat_end',
					'sun_start','sun_end','absent_start', 'absent_end',)

#-----------------------------------------------------------------------------------------
'''
Create new Package
'''
#-----------------------------------------------------------------------------------------
class PackageCreationForm(forms.ModelForm):
	wh_received = forms.ModelChoiceField(label = _("From Warehouse"), queryset=Warehouse.objects.filter(status=True))
	cust_carrier = forms.ChoiceField(label = _("Carrier"), required = True, choices = CARRIER_CHOICE)
	cust_tracking_num = forms.CharField(label = _("Tracking Number"), required = True)

	class Meta:
		model = Service
		fields = (
			'wh_received',
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'no_rush_request',
			'memo',
			)

#-----------------------------------------------------------------------------------------
'''
Create new Co-shipping Package
'''
#-----------------------------------------------------------------------------------------
class CoShippingCreationForm(forms.ModelForm):
	wh_received = forms.ModelChoiceField(label = _("From Warehouse"), queryset=Warehouse.objects.filter(status=True))
	cust_carrier = forms.ChoiceField(label = _("Carrier"), required = True, choices = CARRIER_CHOICE)
	cust_tracking_num = forms.CharField(label = _("Tracking Number"), required = True)

	class Meta:
		model = Service
		fields = (
			'wh_received',
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'receiver',
			'ship_to_col',
			'memo',
			)



#-----------------------------------------------------------------------------------------
'''
Create Direct Shipping Package
'''
#-----------------------------------------------------------------------------------------
class DirectShippingCreationForm(forms.ModelForm):
	wh_received = forms.ModelChoiceField(label = _("From Warehouse"), queryset=Warehouse.objects.filter(status=True))
	cust_carrier = forms.ChoiceField(label = _("Carrier"), required = True, choices = CARRIER_CHOICE)
	cust_tracking_num = forms.CharField(label = _("Tracking Number"), required = True)

	class Meta:
		model = Service
		fields = (
			'wh_received',
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'no_rush_request',
			'ship_to_add',
			'memo',
			)

#-----------------------------------------------------------------------------------------
'''
Create new Item in Package
'''
#-----------------------------------------------------------------------------------------
class ItemForm(forms.ModelForm):
	item_name = forms.CharField(label = 'Item Name',
								widget=forms.TextInput(attrs={
									'placeholder': 'Please enter your items name as detailed as possible',
									}))

	item_detail = forms.CharField( label = 'Item Detail', required=False,
								widget=forms.TextInput(attrs={'placeholder': 'color/size.etc',
								}))

	item_quantity = forms.IntegerField(label = 'quantity',
								widget=forms.NumberInput)

	item_url  = forms.URLField(label = 'Item URL', required=False,
								widget=forms.TextInput(attrs={'placeholder': "https://...",
								}))

	low_volume_request = forms.BooleanField(required=False, label = "Minimize this item's volume")

	memo = forms.CharField( label = 'Note', required=False,
							widget=forms.Textarea(attrs={'placeholder': 'Please enter your needs with this item',
							}))

	class Meta:
		model = Item
		fields = ('item_name', 'item_detail', 'item_quantity', 'item_url', 'low_volume_request', 'memo', )


#-----------------------------------------------------------------------------------------
'''
Item formset in Package
'''
#-----------------------------------------------------------------------------------------
ItemFormset = inlineformset_factory(Service,
									Item,
									form=ItemForm,
									extra=1)

# ItemFormset = inlineformset_factory(Service,
# 									Item,
# 									form=ItemForm,
# 									extra=1,
# 									widgets={'name': Textarea(attrs={'cols': 80, 'rows': 20})}





class SnapshotForm(forms.Form):
	Snapshot = forms.FileField(required = False, widget=forms.ClearableFileInput(attrs={'multiple': True,}))



#-----------------------------------------------------------------------------------------
'''
CoReceiver form in Co-shipping Package
'''
#-----------------------------------------------------------------------------------------
class CoReceiverForm(forms.Form):
	first_name = forms.CharField(required = True, label=_('First Name'))
	last_name = forms.CharField(required = True, label=_('Last Name'))
	phone = forms.CharField(required = True, label=_('phone'), validators=[phone_regex])

	def check(self):
		self.first_name = self.cleaned_data['first_name'].title()
		self.last_name = self.cleaned_data['last_name'].title()
		receivers = CoReceiver.objects.filter(
			first_name = self.first_name,
			last_name = self.last_name,
			phone = self.cleaned_data['phone']
		)
		if receivers.count()>=1:
			return receivers.first()
		else:
			 new = CoReceiver(first_name = self.first_name,
								 last_name = self.last_name,
								 phone = self.cleaned_data['phone'])
			 new.save()
			 return new




class EmailForm(forms.Form):
	email = forms.EmailField(required = True)
	cc = forms.BooleanField(required = False)
	subject = forms.CharField(required = True)
	content = forms.CharField(required = True)

class CartForm(forms.Form):
	package_set = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['package_set'].queryset = Service.objects.filter(user = user, paid_amount = None).order_by('-created_date')

class OrderSetForm(forms.ModelForm):
	class Meta:
		model = OrderSet
		fields = '__all__'
