from django import forms
from main.models import Service, ParentPackage, SHIPPING_CARRIER_CHOICE


from django.utils.translation import gettext as _

class EnterVolumeForm(forms.Form):
	length = forms.IntegerField(required = True, min_value=1)
	width = forms.IntegerField(required = True, min_value=1)
	height = forms.IntegerField(required = True, min_value=1)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['length'].widget.attrs['placeholder'] =_('length')
		self.fields['width'].widget.attrs['placeholder'] =_('width')
		self.fields['height'].widget.attrs['placeholder'] =_('height')


class CoPriceCalForm(forms.ModelForm):

	class Meta:
		model = Service
		fields = (
			'weight',
			'package_type',
			)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['weight'].required = True
		self.fields['package_type'].required = True

class PriceCalForm(forms.ModelForm):

	class Meta:
		model = ParentPackage
		fields = (
			'weight',
			'package_type',
			'carrier',
			)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['weight'].required = True
		self.fields['package_type'].required = True
		self.fields['carrier'].required = True

class IssueForm(forms.Form):
	issue = forms.CharField(required = True)


class ShipCopackageForm(forms.Form):
	package_set = forms.ModelMultipleChoiceField(required = True, queryset=None, widget=forms.CheckboxSelectMultiple())
	tracking_num = forms.CharField(required = True)
	carrier = forms.ChoiceField(required = True, choices=SHIPPING_CARRIER_CHOICE)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['package_set'].queryset = Service.objects.filter(co_shipping = True, parent_package__shipped_date = None).exclude(paid_amount=None)
