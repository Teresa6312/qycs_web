from django import forms
from .models import (
	User, Address, Service, CollectionPoint, Warehouse,
	Item, PackageSnapshot, CoReceiver, FavoriteWebsite,
	CARRIER_CHOICE, phone_regex, OrderSet, LANGUAGE_CATEGORY, SHIPPING_CARRIER_CHOICE
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
				years = birthday_years,
				attrs={"class":"w3-quarter w3-border"}))

	first_name = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	last_name = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	email = forms.EmailField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	phone = forms.CharField(required = True, validators=[phone_regex], widget=forms.TextInput(attrs={'placeholder': _('+1-234-567-8900'),"class":"w3-input w3-border"
									}))
	country = forms.CharField(required = False, initial='USA',  widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	language = forms.ChoiceField(required = False, choices = LANGUAGE_CATEGORY,
									widget=forms.Select(attrs={"class":"w3-select w3-border"
									}))
	username = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))

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
	first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	last_name = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	email = forms.EmailField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	phone = forms.CharField(required = True, validators=[phone_regex], widget=forms.TextInput(attrs={'placeholder': _('+1-234-567-8900'),"class":"w3-input w3-border"
																									}))
	address = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder':  _("Street Address"),
																		"class":"w3-input w3-border"
																		}))
	apt = forms.CharField(required = False, widget=forms.TextInput(attrs={'placeholder':  _("Apartment/Suit/Unit"),
																		"class":"w3-input w3-border"
																		}))
	city = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	state = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	country = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	zipcode = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	location_name = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))

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


#-----------------------------------------------------------------------------------------
'''
Create new Package
'''
#-----------------------------------------------------------------------------------------

class PackageCommonForm(forms.ModelForm):
	wh_received = forms.ModelChoiceField(label = _("From Warehouse"), queryset=Warehouse.objects.filter(status=True),
									widget=forms.Select(attrs={"class":"w3-select w3-border"
									}))
	cust_carrier = forms.ChoiceField(label = _("Carrier"), required = True, choices = CARRIER_CHOICE,
									widget=forms.Select(attrs={"class":"w3-select w3-border"
									}))
	cust_tracking_num = forms.CharField(label = _("Tracking Number"), required = True,
									widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	memo = forms.CharField(label = 'Note', required=False,
							widget=forms.Textarea(attrs={'placeholder':  _("Please enter your needs with this package"),
												"class":"w3-input w3-border",
												"rows":5
												}))
	low_volume_request = forms.BooleanField(label = _("Minimize your package's volume"), required=False)

	class Meta:
		abstract = True

class PackageCreationForm(PackageCommonForm):

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
class CoShippingCreationForm(PackageCommonForm):
	no_rush_request = forms.BooleanField(label = _("No Rush Shipping (Double Points)"), required=False)
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
class DirectShippingCreationForm(PackageCommonForm):
	ship_carrier = forms.ChoiceField(label = _("Select a Carrier"), required = True, choices = SHIPPING_CARRIER_CHOICE,
									widget=forms.Select(attrs={"class":"w3-select w3-border"
									}))
	class Meta:
		model = Service
		fields = (
			'wh_received',
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'no_rush_request',
			'ship_carrier',
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
									"class":"w3-input w3-border item_name"
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

	low_volume_request = forms.BooleanField(required=False)

	memo = forms.CharField( label = 'Note', required=False,
							widget=forms.Textarea(attrs={'placeholder': 'Please enter your needs with this item',
												"class":"w3-input w3-border",
												"rows": 3 }))

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

class TrackingForm(forms.Form):
	cust_tracking_num = forms.CharField(required = True)



#-----------------------------------------------------------------------------------------
'''
CoReceiver form in Co-shipping Package
'''
#-----------------------------------------------------------------------------------------
class CoReceiverForm(forms.Form):
	first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': _('First Name'),"class":"w3-input w3-border"}))
	last_name = forms.CharField(required = True,  widget=forms.TextInput(attrs={'placeholder': _('Last Name'),"class":"w3-input w3-border"}))
	phone = forms.CharField(required = True, validators=[phone_regex], widget=forms.TextInput(attrs={'placeholder': _('Phone Number (+1-234-567-8900)'),"class":"w3-input w3-border"}))

	def __init__(self, receiver=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if receiver:
			self.fields['first_name'].initial = receiver.first_name
			self.fields['last_name'].initial = receiver.last_name
			self.fields['phone'].initial = receiver.phone



class CoReceiverCheckForm(forms.Form):
	first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': _('First Name'),"class":"w3-input w3-border"}))
	last_name = forms.CharField(required = True,  widget=forms.TextInput(attrs={'placeholder': _('Last Name'),"class":"w3-input w3-border"}))
	phone = forms.CharField(required = True, validators=[phone_regex], widget=forms.TextInput(attrs={'placeholder': _('Phone Number (+1-234-567-8900)'),"class":"w3-input w3-border"}))

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
