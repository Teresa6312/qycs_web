from django import forms
from .models import (
	User, Address, Service, CollectionPoint, Warehouse,
	Item, PackageSnapshot, CoReceiver, FavoriteWebsite,
	CARRIER_CHOICE,
	)
# from django.core.exceptions import ObjectDoesNotExist, NON_FIELD_ERRORS
#used to catch errors related to populating the form fields from a related Project

from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

import datetime

year = datetime.datetime.now().year
years = [i for i in range(year-100,year)]

class NewUserCreationForm(UserCreationForm):
	birthday = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = years))
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
				years = years))

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
				if user.email_confirmed:
					self.fields['email'].widget.attrs['readonly'] = True
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
	class Meta:
		model = CollectionPoint
		fields = ('store','store_name','license_type', 'license_image','id_image',
					'address','apt','city','state','country','zipcode',
					'collector_icon', 'name', 'wechat', 'wechat_qrcode',
					'referrer', 'apply_reason', 'info_source',)

class ColChangeForm(forms.ModelForm):
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
			'ship_to_col',
			'receiver',
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
									"class":"w3-input w3-border"
									}))

	item_detail = forms.CharField( label = 'Item Detail', required=False,
								widget=forms.TextInput(attrs={'placeholder': 'color/size.etc',
								"class":"w3-input w3-border"
								}))

	item_quantity = forms.IntegerField(label = 'quantity',
								widget=forms.NumberInput(attrs={"class":"w3-input w3-border"}))

	item_url  = forms.URLField(label = 'Item URL', required=False,
								widget=forms.TextInput(attrs={'placeholder': "https://...",
																"class":"w3-input w3-border"
																}))

	low_volume_request = forms.BooleanField(required=False, label = "Minimize this item's volume")

	memo = forms.CharField( label = 'Note', required=False,
							widget=forms.Textarea(attrs={'placeholder': 'Please enter your needs with this item',
												"class":"w3-input w3-border"}))

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
class CoReceiverForm(forms.ModelForm):

	def save(self, user, commit = True):
		newreceiver = super(CoReceiverForm, self).save(commit = False)
		newreceiver.first_name = newreceiver.first_name.title()
		newreceiver.last_name = newreceiver.last_name.title()
		if commit:
			receivers = CoReceiver.objects.filter(
				first_name = newreceiver.first_name,
				last_name = newreceiver.last_name,
				phone = newreceiver.phone,
			)
			if receivers.count()>=1:
				return receivers.first()
			else:
				newreceiver.save()
			return newreceiver

	class Meta:
		model = CoReceiver
		fields = ('first_name', 'last_name', 'phone')


class EmailForm(forms.Form):
	email = forms.EmailField(required = True)
	cc = forms.BooleanField(required = False)
	subject = forms.CharField(required = True)
	content = forms.CharField(required = True)
