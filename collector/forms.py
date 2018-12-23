from django import forms
from .models import Review, Question
from django.utils.translation import gettext as _
from main.models import CollectionPoint, INFORMATION_SOURCES
from main.forms import schedule_years

class MessageForm(forms.Form):
	message = forms.CharField(required=True)

class ResponseForm(forms.Form):
	response = forms.CharField(required=True)
	response_for = forms.IntegerField(required=True)

class ColCreationForm(forms.ModelForm):

	class Meta:
		model = CollectionPoint
		fields = ('store','store_name','license_type', 'license_image','id_image',
					'address','apt','city','state','country','zipcode',
					'collector_icon', 'name', 'wechat', 'wechat_qrcode',
					'referrer', 'apply_reason', 'info_source','agreement', 'paypal')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['apt'].widget.attrs['placeholder'] = _('Apartment/Suit/Unit')
		self.fields['address'].widget.attrs['placeholder'] = _('Street Address')
		self.fields['apply_reason'].widget.attrs['placeholder'] =  _("Please tell us why you want to join us")
		self.fields['info_source'].choices = INFORMATION_SOURCES
		self.fields['apply_reason'].widget.attrs['rows'] = 3
		self.fields['agreement'].required = True


class ColChangeForm(forms.ModelForm):
	absent_start = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("YYYY", "MM", "DD"),
					years = schedule_years))
	absent_end = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("YYYY", "MM", "DD"),
					years = schedule_years))

	class Meta:
		model = CollectionPoint
		fields = ('collector_icon', 'wechat', 'wechat_qrcode','description','show_contact',
					'mon_start', 'mon_end', 'tue_start', 'tue_end',
					'wed_start','wed_end','thu_start','thu_end',
					'fri_start','fri_end','sat_start','sat_end',
					'sun_start','sun_end','absent_start', 'absent_end',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['description'].widget.attrs['placeholder'] = _("Introduce yourself. This will show up in the website.")
		self.fields['description'].widget.attrs['rows'] = 3
		for field_name in ['mon_start','tue_start','wed_start','thu_start','fri_start','sat_start','sun_start']:
			self.fields[field_name].widget.attrs['placeholder'] =  _('From: 00:00')
		for field_name in ['mon_end','tue_end','wed_end','thu_end','fri_end','sat_end','sun_end']:
			self.fields[field_name].widget.attrs['placeholder'] =  _('Until: 23:59')
