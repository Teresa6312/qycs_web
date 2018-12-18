from django import forms
from main.models import Service


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


class PriceCalForm(forms.ModelForm):

	class Meta:
		model = Service
		fields = (
			'weight',
			'ship_carrier',
			'package_type',
			)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['weight'].required = True
		self.fields['ship_carrier'].required = True
		self.fields['package_type'].required = True
