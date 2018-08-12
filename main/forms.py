from django import forms
from .models import (
	User, UserProfile, Address, Service, Warehouse, CollectionPoint,
	Item, PackageImage, CoReceiver, FavoriteWebsite
	)
from django.core.exceptions import ObjectDoesNotExist, NON_FIELD_ERRORS
#used to catch errors related to populating the form fields from a related Project

from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from .code import checkAddress, boundEmail
from django.forms import formset_factory
# import datetime
# datetime.datetime.now().year

years = [i for i in range(1900,2010)]

 # fields = '__all__'
 # exclude = ['title']
	 # class Meta:
	 #    model = Author
	 #    fields = ('name', 'title', 'birth_date')
	 #    widgets = {
	 #        'name': Textarea(attrs={'cols': 80, 'rows': 20}),
	 #    }
	 #     labels = {
	 #        'name': _('Writer'),
	 #    }
	 #    help_texts = {
	 #        'name': _('Some useful help text.'),
	 #    }
	 #    error_messages = {
	 #        'name': {
	 #            'max_length': _("This writer's name is too long."),
	 #        },
	 #    }
	 #
	# self.fields['sku'].widget.attrs['readonly'] = True
#-----------------------------------------------------------------------------------------
'''
Create User
'''
#-----------------------------------------------------------------------------------------
class RegisterForm(UserCreationForm):
	first_name = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	last_name = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	username = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	email = forms.EmailField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	password1 = forms.CharField(required = True, widget=forms.PasswordInput(attrs={"class":"w3-input w3-border"
									}))
	password2 = forms.CharField(required = True, widget=forms.PasswordInput(attrs={"class":"w3-input w3-border"
									}))

	class Meta(UserCreationForm.Meta):
		fields = ['username', 'email', 'first_name','last_name', 'password1', 'password2']
		# error_messages = {
		#     NON_FIELD_ERRORS: {
		#         'unique': "%(model_name)s's %(field_labels)s is not unique.",
		#     }
		# }

	def save(self, commit = True, *args, **kwargs):
		user = super().save(commit = False)
		if commit:
			user.first_name = self.cleaned_data['first_name'].title()
			user.last_name = self.cleaned_data['last_name'].title()
			user.email = self.cleaned_data['email'].lower()
			user.username = self.cleaned_data['username']
			user.save()
		return user

	def clean_email(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		if email and User.objects.filter(email=email).exclude(username=username).exists():
			raise forms.ValidationError(u'Email addresses must be unique.')
		return email


class ColResigterForm(forms.ModelForm):
	address = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	apt = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	city = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	state = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	country = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	zipcode = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	license = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	license_type = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	store = forms.BooleanField(required = False, widget=forms.CheckboxInput(attrs={"class":"w3-check"
									}))
	store_name = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	license_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={"class":"w3-input w3-border"
									}))
	id_image = forms.ImageField(required=True, widget=forms.FileInput(attrs={"class":"w3-input w3-border"
									}))
	location_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class":"w3-input w3-border"
									}))
	class Meta:
		model = CollectionPoint
		fields = ['address','apt','city','state','country','zipcode','license','license_type',
					'store','store_name','store_name','license_image','id_image','location_image']

class FavoriteWebsiteForm(forms.ModelForm):

	TYPE_CHOICE = (
		('---', '---'),
		('Clothing', 'Clothing'),
		('Bag', 'Bag'),
		('Jewelry', 'Jewelry'),
		('Sport', 'Sport'),
		('Beauty', 'Beauty'),
		('Baby', 'Baby'),
		('Other', 'Other'),
	)

	web_type = forms.ChoiceField(required = True, choices = TYPE_CHOICE, widget=forms.Select(attrs={"class":"w3-select w3-border"
				}))
	web_name = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
				}))
	class Meta:
		model = FavoriteWebsite
		fields = ['web_type', 'web_name']

WebFormSet = formset_factory(FavoriteWebsiteForm, extra = 3, max_num = 3)

class UserProfileForm(forms.ModelForm):
	country = forms.CharField(required = True, initial='USA',  widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	birthday = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = years,
					attrs={"class":"w3-input w3-border w3-third",
									}))
	phone = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	language = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))

	class Meta:
		model = UserProfile
		fields = ['country', 'birthday', 'phone', 'language']



#-----------------------------------------------------------------------------------------
'''
Use in Update User Profile or Register as Collector
'''
#-----------------------------------------------------------------------------------------
class ProfileForm(forms.Form):
	first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	last_name = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	email = forms.EmailField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	phone = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	birthday = forms.DateField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	country = forms.CharField(required = True, initial='USA',  widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	language = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))

	def save(self, user, commit = True):
		profile = UserProfile.objects.get(user = user)
		if commit:
# disable tag make the field as '', need to asign the first_name and last_name when it is ''
			if user.first_name != self.cleaned_data['first_name'].title() and user.last_name != self.cleaned_data['last_name'].title():
				user.first_name = self.cleaned_data['first_name'].title() or user.first_name
				user.last_name = self.cleaned_data['last_name'].title() or user.last_name

			if self.cleaned_data['email'] !='' and self.cleaned_data['email'] != None:
				user.email = self.cleaned_data['email'].lower()
# send email to bound this email
			user.save()

# -------------------------------------------------------------------------------------------
# '''
# Update the UserProfile
# '''
# ------------------------------------------------------------------------------------------
			profile.country = self.cleaned_data['country'] or profile.birthday
			profile.country = self.cleaned_data['language'] or profile.language
			profile.birthday = self.cleaned_data['birthday'] or profile.birthday
			profile.phone = self.cleaned_data['phone'] or profile.phone
			profile.save()
		return user


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
	phone = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	address = forms.CharField(required = True, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
	apt = forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"w3-input w3-border"
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
		exclude = ['meno']

	def save(self, commit=True, *args, **kwargs):
		add = super(AddressForm, self).save(commit=False, *args, **kwargs)
		add.first_name = add.first_name.title()
		add.last_name = add.last_name.title()
		add.email = add.email.lower()
		add.address = add.address.upper()
		add.apt = add.apt.upper()
		add.city = add.city.upper()
		add.state = add.state.upper()
		add.country = add.country.upper()
		if commit:
			add.save()
		return add
#-----------------------------------------------------------------------------------------
'''
Package Common Form (abstract)
'''
#-----------------------------------------------------------------------------------------
class PackageCommonForm(forms.ModelForm):
	# TYPE_CHOICE = (
	# 	('Food', 'Food'),
	# 	('Regular', 'Regular'),
	# 	('Luxury', 'Luxury'),
	# 	('Mix', 'Mix'),
	# # )
	# COUNTRY_CHOICE = (
	# 	('China', 'China'),
	# )

	CARRIER_CHOICE = (
		('ZhongTong', 'ZhongTong'),
	)

	# package_type = forms.ChoiceField(choices = TYPE_CHOICE)
	# # wh_received = forms.ModelChoiceField(queryset = Warehouse.objects.all(), label = "From Warehouse")

	# shoule be related to the wh_received
	cust_carrier = forms.ChoiceField(label = "Mailing Carriers", choices = CARRIER_CHOICE,
									widget=forms.Select(attrs={"class":"w3-select w3-border"
									}))
	cust_tracking_num = forms.CharField(label = "Tracking Number",
									widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))

	low_volume_request = forms.BooleanField(label = "Minimize your package's volume", required=False)
	no_rush_request = forms.BooleanField(label = "No Rush Shipping (Double Points)", required=False)
	memo = forms.CharField(label = 'Note', required=False,
							widget=forms.Textarea(attrs={'placeholder': 'Please enter your needs with this package',
												"class":"w3-input w3-border"
												}))

	class Meta:
		abstract = True



#-----------------------------------------------------------------------------------------
'''
Create new Package
'''
#-----------------------------------------------------------------------------------------
class PackageForm(PackageCommonForm):


	class Meta:
		model = Service
		fields = (
			# 'wh_received',
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
class CoShippingForm(PackageCommonForm):

	class Meta:
		model = Service
		fields = ('cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'no_rush_request',
			'memo',
			'ship_to_add',
			)



#-----------------------------------------------------------------------------------------
'''
Create Direct Shipping Package
'''
#-----------------------------------------------------------------------------------------
class DirectShippingForm(PackageCommonForm):

	class Meta:
		model = Service
		fields = (
			'cust_carrier',
			'cust_tracking_num',
			'low_volume_request',
			'no_rush_request',
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





#-----------------------------------------------------------------------------------------
'''
Image form and formset in Package
'''
#-----------------------------------------------------------------------------------------
class PackageImageForm(forms.ModelForm):
	package = forms.ModelChoiceField(queryset=Service.objects.all())
	image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class":"w3-input w3-border"}))
	class Meta:
		model = PackageImage
		fields = ('image','package')

ImageFormset = inlineformset_factory(Service,
									PackageImage,
									form=PackageImageForm,
									extra=1)

class ImageForm(forms.Form):
	image = forms.FileField(required = False, widget=forms.ClearableFileInput(attrs={'multiple': True, "class":"w3-input w3-border"}))



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
			elif newreceiver.first_name==user.first_name and newreceiver.last_name==user.last_name and user.userprofile.phone==newreceiver.phone:
				return CoReceiver.objects.get(user=user)
			else:
				newreceiver.user = None
				newreceiver.save()
				return newreceiver
	class Meta:
		model = CoReceiver
		fields = ('first_name', 'last_name', 'phone')





# class ContactForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         assigned_users = kwargs.pop('assigned_to', [])
#         contact_account = kwargs.pop('account', [])
#         super(ContactForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs = {"class": "form-control"}
#         self.fields['description'].widget.attrs.update({
#             'rows': '6'})
#         self.fields['assigned_to'].queryset = assigned_users
#         self.fields['account'].queryset = contact_account
#         self.fields['assigned_to'].required = False
#         self.fields['teams'].required = False

#     class Meta:
#         model = Contact
#         fields = (
#             'assigned_to', 'teams', 'first_name', 'last_name', 'account', 'email', 'phone', 'address', 'description'
#         )

#     def clean_phone(self):
#         client_phone = self.cleaned_data.get('phone', None)
#         try:
#             if int(client_phone) and not client_phone.isalpha():
#                 ph_length = str(client_phone)
#                 if len(ph_length) < 10 or len(ph_length) > 13:
#                     raise forms.ValidationError('Phone number must be minimum 10 Digits and maximum of 13 Digits')
#         except (ValueError):
#             raise forms.ValidationError('Phone Number should contain only Numbers')
#         return client_phone
