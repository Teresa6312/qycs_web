from django import forms
from .models import Review, Question
from django.utils.translation import gettext as _
from main.models import CollectionPoint
from main.forms import schedule_years
from cloudinary.forms import CloudinaryJsFileField

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
					'referrer', 'apply_reason', 'info_source','agreement')

	agreement = forms.BooleanField(required = True, label = _("Agree"))
	license_image = CloudinaryJsFileField()
	id_image = CloudinaryJsFileField()
	collector_icon = CloudinaryJsFileField()
	wechat_qrcode = CloudinaryJsFileField()


class ColChangeForm(forms.ModelForm):
	class Meta:
		model = CollectionPoint
		fields = ('collector_icon', 'wechat', 'wechat_qrcode','description','show_contact',
					'mon_start', 'mon_end', 'tue_start', 'tue_end',
					'wed_start','wed_end','thu_start','thu_end',
					'fri_start','fri_end','sat_start','sat_end',
					'sun_start','sun_end','absent_start', 'absent_end',)
						
	collector_icon = CloudinaryJsFileField()
	wechat_qrcode = CloudinaryJsFileField()
	absent_start = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = schedule_years,
					attrs={"class":"w3-quarter w3-border"}))
	absent_end = forms.DateField(required = False, widget=forms.SelectDateWidget(
					empty_label=("Year", "Month", "Day"),
					years = schedule_years,
					attrs={"class":"w3-quarter w3-border"}))

	mon_start = forms.TimeField(required = False, label= _('Monday'), widget=forms.TextInput(attrs={'placeholder': _('From: 00:00:00'),"class":"w3-input w3-border"
																									}))
	mon_end = forms.TimeField(required = False, widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	tue_start = forms.TimeField(required = False, label= _('Tuesday'), widget=forms.TextInput(attrs={'placeholder': _('From:  00:00:00'),"class":"w3-input w3-border"
																									}))
	tue_end = forms.TimeField(required = False, widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	wed_start = forms.TimeField(required = False, label= _('Wednesday'), widget=forms.TextInput(attrs={'placeholder': _('From: 00:00:00'),"class":"w3-input w3-border"
																									}))
	wed_end = forms.TimeField(required = False, widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	thu_start = forms.TimeField(required = False, label= _('Thursday'), widget=forms.TextInput(attrs={'placeholder': _('From:  00:00:00'),"class":"w3-input w3-border"
																									}))
	thu_end = forms.TimeField(required = False, widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	fri_start = forms.TimeField(required = False, label= _('Friday'), widget=forms.TextInput(attrs={'placeholder': _('From: 00:00:00'),"class":"w3-input w3-border"
																									}))
	fri_end = forms.TimeField(required = False,  widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	sat_start = forms.TimeField(required = False, label= _('Saturday'), widget=forms.TextInput(attrs={'placeholder': _('From: 00:00:00'),"class":"w3-input w3-border"
																									}))
	sat_end = forms.TimeField(required = False, widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	sun_start = forms.TimeField(required = False, label= _('Sunday'), widget=forms.TextInput(attrs={'placeholder': _('From: 00:00:00'),"class":"w3-input w3-border"
																									}))
	sun_end = forms.TimeField(required = False, widget=forms.TextInput(attrs={'placeholder': _('Unitl: 00:00:00'),"class":"w3-input w3-border"
																									}))
	description = forms.CharField(label = 'Introduction', required=False,
							widget=forms.Textarea(attrs={'placeholder':  _("Introduce yourself. This will show up in the website."),
												"class":"w3-input w3-border",
												"rows":5
												}))
	wechat = forms.CharField(label = _("Wechat ID"), required = False,
									widget=forms.TextInput(attrs={"class":"w3-input w3-border"
									}))
