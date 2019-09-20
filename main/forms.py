from django import forms
from .models import (
	User, Address, Service, CollectionPoint, Warehouse, ParentPackage,
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
						empty_label=("YYYY", "MM", "DD"),
					years = birthday_years))
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username', 'email', 'first_name', 'last_name',
					'phone', 'country', 'language', 'birthday', 'password1', 'password2', 'privacy_policy_agree')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['birthday'].label = _('Birthday')
		self.fields['country'].initial = 'USA'
		self.fields['phone'].validators = [phone_regex]
		self.fields['language'].choices = LANGUAGE_CATEGORY
		self.fields['phone'].widget.attrs['placeholder'] = _('+1-234-567-8900')
		self.fields['privacy_policy_agree'].required = True

	def save(self, commit=True, *args, **kwargs):
		user = super(NewUserCreationForm, self).save(commit=False, *args, **kwargs)
		user.first_name = user.first_name.title()
		user.last_name = user.last_name.title()
		user.email = user.email.lower()
		if commit:
			user.save()
		return user

class NewUserChangeForm(UserChangeForm):
	birthday = forms.DateField(required = False, widget=forms.SelectDateWidget(
				empty_label=("YYYY", "MM", "DD"),
				years = birthday_years))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name',
					'phone', 'country', 'language', 'birthday',
					'default_address', 'default_col', 'password',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['birthday'].label = _('Birthday')
		self.fields['country'].initial = 'USA'
		self.fields['phone'].validators = [phone_regex]
		self.fields['language'].choices = LANGUAGE_CATEGORY
		self.fields['phone'].widget.attrs['placeholder'] = _('+1-234-567-8900')
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

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['apt'].widget.attrs['placeholder'] = _('Apartment/Suit/Unit')
		self.fields['phone'].widget.attrs['placeholder'] = _('+1-234-567-8900')
		self.fields['phone'].validators = [phone_regex]
		self.fields['address'].widget.attrs['placeholder'] = _('Street Address')


	def save(self, commit=True, *args, **kwargs):
		add = super(AddressForm, self).save(commit=False, *args, **kwargs)
		add.first_name = add.first_name.title()
		add.last_name = add.last_name.title()
		add.address = add.address.title()
		add.apt = add.apt.title()
		add.city = add.city.title()
		add.state = add.state.title()
		if commit:
			add.save()
		return add


#-----------------------------------------------------------------------------------------
'''
Create new Package
'''
#-----------------------------------------------------------------------------------------
class PackageCreationForm(forms.ModelForm):

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
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['memo'].widget.attrs['placeholder'] =_("Please enter your needs about this package")
		self.fields['memo'].widget.attrs['rows'] = 5
		self.fields['wh_received'].queryset=Warehouse.objects.filter(status=True)
		self.fields['wh_received'].required = True


#-----------------------------------------------------------------------------------------
'''
Create new Co-shipping Package
'''
#-----------------------------------------------------------------------------------------
class CoShippingCreationForm(forms.ModelForm):
	class Meta:
		model = Service
		fields = (
			'wh_received',
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'no_rush_request',
			'receiver',
			'ship_to_col',
			'memo',
			)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['memo'].widget.attrs['placeholder'] =_("Please enter your needs about this package")
		self.fields['memo'].widget.attrs['rows'] = 5
		self.fields['wh_received'].queryset=Warehouse.objects.filter(status=True)
		self.fields['wh_received'].required = True
		self.fields['cust_carrier'].required = True
		self.fields['cust_tracking_num'].required = True
		self.fields['ship_to_col'].required = True


#-----------------------------------------------------------------------------------------
'''
Create Direct Shipping Package
'''
#-----------------------------------------------------------------------------------------
class DirectShippingCreationForm(forms.ModelForm):
	class Meta:
		model = Service
		fields = (
			'wh_received',
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'ship_carrier',
			'ship_to_add',
			'memo',
			)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['memo'].widget.attrs['placeholder'] =_("Please enter your needs about this package")
		self.fields['memo'].widget.attrs['rows'] = 5
		self.fields['wh_received'].queryset=Warehouse.objects.filter(status=True)
		self.fields['wh_received'].required = True
		self.fields['cust_carrier'].required = True
		self.fields['cust_tracking_num'].required = True
		self.fields['ship_to_add'].required = True
		self.fields['ship_carrier'].required = True
		self.fields['ship_carrier'].label = _("Select a Carrier")
		self.fields['ship_carrier'].choices =SHIPPING_CARRIER_CHOICE

class PackageChangeForm(forms.ModelForm):
		class Meta:
			model = Service
			fields = (
				'ship_carrier',
				'ship_to_add',
				'ship_to_col',
				'receiver',
				'memo',
				)
#-----------------------------------------------------------------------------------------
'''
Create new Item in Package
'''
#-----------------------------------------------------------------------------------------
class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('item_name', 'item_detail', 'item_quantity', 'item_url', 'low_volume_request', 'memo', )

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['memo'].widget.attrs['placeholder'] =_("Please enter your needs with this item")
		self.fields['memo'].widget.attrs['rows'] = 5
		self.fields['item_url'].widget.attrs['placeholder'] ="http://..."
		self.fields['item_detail'].widget.attrs['placeholder'] =_('color/size.etc')
		self.fields['item_name'].widget.attrs['placeholder'] = _("Please enter your items' name as detailed as possible")

#-----------------------------------------------------------------------------------------
'''
Item formset in Package
'''
#-----------------------------------------------------------------------------------------
ItemFormset = inlineformset_factory(Service,
									Item,
									form=ItemForm,
									extra=1)

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
	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)
	phone = forms.CharField(required = True)

	def __init__(self, receiver=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs['placeholder'] =_('First Name')
		self.fields['last_name'].widget.attrs['placeholder'] =_('Last Name')
		self.fields['phone'].widget.attrs['placeholder'] ='(+1)234-567-8900'
		self.fields['phone'].validators = [phone_regex]
		if receiver:
			self.fields['first_name'].initial = receiver.first_name
			self.fields['last_name'].initial = receiver.last_name
			self.fields['phone'].initial = receiver.phone




class CoReceiverCheckForm(forms.Form):
	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)
	phone = forms.CharField(required = True)

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
	package_set = forms.ModelMultipleChoiceField(required = False, queryset=None, widget=forms.CheckboxSelectMultiple())
	parent_package_set = forms.ModelMultipleChoiceField(required = False, queryset=None, widget=forms.CheckboxSelectMultiple())

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['package_set'].queryset = Service.objects.filter(user = user, paid_amount = None)
		self.fields['parent_package_set'].queryset = ParentPackage.objects.filter(paid_amount = None)

class OrderSetForm(forms.ModelForm):
	class Meta:
		model = OrderSet
		fields = '__all__'
