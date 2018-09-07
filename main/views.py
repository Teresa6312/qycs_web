from .models import (
	Address, Service, CollectionPoint, Resource,
	User, Warehouse, FavoriteWebsite, Location
	)
from .forms import (
	NewUserCreationForm, NewUserChangeForm, AddressForm, WebFormSet,
	ColCreationForm, EmailForm, ColChangeForm
	)

from .code import send_confirmation_email

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.urls import reverse
# used to reverse the url name as a url path

from django.conf import settings
from django.http import QueryDict
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
import os
import json
# from django.core import serializers
from django.utils.translation import gettext as _
from django.db import IntegrityError

from django.db import IntegrityError
from django.core.serializers.json import DjangoJSONEncoder


class HomeView(TemplateView):
	template_name = 'main/home.html'

	def get(self, request):
		return render(request, self.template_name)


class RegisterView(TemplateView):
	template_name = 'main/register.html'

	def get(self, request):
		form = NewUserCreationForm()
		webformset = WebFormSet()
		return render(request, self.template_name, {'form': form, 'webformset':webformset})

	def post(self, request):
		form = NewUserCreationForm(request.POST)
		webformset = WebFormSet(request.POST)

		if form.is_valid() and webformset.is_valid():
			user = form.save()
			for webform in webformset:
				web = webform.save(commit = False)
				web.country = user.country
				web.web_name = web.web_name.title()

				if webform.is_valid():
					existed_web = FavoriteWebsite.objects.filter(
						web_name = web.web_name,
						web_type = web.web_type,
						country = user.country)

					if existed_web.count() == 1:
						existed_web = existed_web.first()
						existed_web.rate = existed_web.rate +1
						existed_web.save()
					else:
						web.save()
			try:
				send_confirmation_email(request, user)
				messages.info(request, _('Confirmation link was sent successfully. Please check your email!'))
			except:
				messages.error(request, _('Confirmation link was fail to send!'))


			username = request.POST['username']
			password = request.POST['password1']
			login_user = authenticate(
				username = username,
				password = password
			)
			login(request, login_user)

			if "colregister" in request.POST:
				return redirect(reverse('colregister'))
			else:
				return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {'form': form, 'webformset':webformset})

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.email_confirmed = True
		user.save()
		login(request, user, backend)
		return redirect('account')
	else:
		return HttpResponse('Activation link is invalid!')

def sendConfirmationEmail(request):
	if request.user.email:
		try:
			send_confirmation_email(request, request.user)
			messages.info(request, _('Confirmation link was sent successfully. Please check your email!'))
		except:
			messages.error(request, _('Confirmation link was fail to send!'))
	else:
		messages.error(request, _('Failure! Please check your email.'))
	return redirect('account')



class SendEmailView(TemplateView):

	def post(self, request):
		email = EmailForm(request.POST)
		next = request.POST.get('next','')
		if email.is_valid():
			user_email = email.cleaned_data['email'].lower()
			subject = _('Contact us - ') + email.cleaned_data['subject']
			content = _('From ') + user_email + '\n' + email.cleaned_data['content']
			to_email = ['myqycs.001@gmail.com',]
			if email.cleaned_data['cc']:
				to_email.append(user_email)

			send_mail(
					subject,
					content,
					settings.EMAIL_HOST_USER,
					to_email,
					fail_silently=False,
				)
		if next and next!='':
			return redirect(next)
		else:
			return redirect(reverse('home'))


class ColRegisterView(TemplateView):
	template_name = 'main/colregister.html'

	def get(self, request):
		userform = NewUserChangeForm(instance=request.user)
		userform.fields['password'].required = False
		userform.fields['phone'].required = True
		userform.fields['first_name'].required = True
		userform.fields['last_name'].required = True
		colform = ColCreationForm()
		try:
			text = Resource.objects.get(title='colregister')
			term = text.english_content
		except:
			term = _('Term is not avaliable Right now.')

		return render(request, self.template_name, {'colform': colform,
													'userform': userform,
													"term": term,
													})

	def post(self, request):
		userform  = NewUserChangeForm(request.POST, instance=request.user)
		userform.fields['password'].required = False
		colform = ColCreationForm(request.POST, request.FILES)
		if colform.is_valid() and userform.is_valid():
			user = userform.save(request.user)
			collector = colform.save(commit=False)
			collector.collector = user
			collector.save()
			user.default_col = collector
			user.save()
			messages.info(request, _('Thank you for applied collection point. We will process your application in a week.'))
			return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {
					 'colform': colform,
					 'userform': userform,
					 })

class CollectorUpdateView(TemplateView):
	template_name = 'main/collector_update.html'

	def get(self, request):
		if request.user.collectionpoint:
			form = ColChangeForm(instance = request.user.collectionpoint)
			return render(request, self.template_name, {'form': form})
		else:
			return redirect(reverse('colregister'))

	def post(self, request):
		try:
			col = CollectionPoint.objects.get(collector = request.user)
			form = ColChangeForm(request.POST, request.FILES, instance=col)
			if form.is_valid():
				form.save()
				return redirect(reverse('account'))
		except:
# to the prev page create next for each views
			pass
		else:
			return render(request, self.template_name, {'form': form,
														})

class AccountView(TemplateView):
	template_name = 'main/account.html'

	def get(self, request):
		return render(request, self.template_name)

# -----------------------------------------------------------
'''
Update User Profile
'''
# -----------------------------------------------------------
class UpdateProfileView(TemplateView):
	template_name = 'main/updateprofile.html'
	col_list = CollectionPoint.objects.filter(status=True)

	def get(self, request):
		form = NewUserChangeForm(instance=request.user)
		form.fields['password'].required = False
		return render(request, self.template_name, { 'form': form,
													'col_list': self.col_list,
													})

	def post(self, request):
		form = NewUserChangeForm(request.POST, instance=request.user)
		form.fields['password'].required = False
		if form.is_valid():
			user = form.save()
			return redirect(reverse('account'), user = user)
		else:
			return render(request, self.template_name, {
									'col_list': self.col_list,
									'form': form
									})

class ChangePasswordView(TemplateView):
	template_name = 'main/changepassword.html'

	def get(self, request):
		form = PasswordChangeForm(user = request.user)
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = PasswordChangeForm(data = request.POST, user = request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {'form': form})


def locationView(request):
	if request.POST:
		field=request.POST.get('field','')
		value=request.POST.get('value','')
		if field=="id_country":
			locations=[i['country'] for i in Location.objects.filter(country__startswith=value).values('country').distinct()]
			locationsA=[i['state'] for i in Location.objects.filter(country__startswith=value).values('state').distinct()]
			locationsB=[i['city'] for i in Location.objects.filter(country__startswith=value).values('city').distinct()]
			context = json.dumps({
			'data': locations,
			'state': locationsA,
			'city': locationsB})
			return HttpResponse(context, content_type='application/json')
		elif field=="id_state":
			locations=[i['state'] for i in Location.objects.filter(state__startswith=value).values('state').distinct()]
			locationsA=[i['country'] for i in Location.objects.filter(state__startswith=value).values('country').distinct()]
			locationsB=[i['city'] for i in Location.objects.filter(state__startswith=value).values('city').distinct()]
			context = json.dumps({
			'data': locations,
			'country': locationsA,
			'city': locationsB})
			return HttpResponse(context, content_type='application/json')
		elif field=="id_city":
			locations=[i['city'] for i in Location.objects.filter(city__startswith=value).values('city').distinct()]
			locationsA=[i['country'] for i in Location.objects.filter(city__startswith=value).values('country').distinct()]
			locationsB=[i['state'] for i in Location.objects.filter(city__startswith=value).values('state').distinct()]
			context = json.dumps({
			'data': locations,
			'country': locationsA,
			'state': locationsB})
			return HttpResponse(context, content_type='application/json')

class AddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request):
		addform = AddressForm()
		return render(request, self.template_name, {'addform': addform,})

	def post(self, request):
		add_field_name=request.POST.get('add_field_name','')

		if "addform" in request.POST:
			addform = AddressForm(QueryDict(request.POST.get('addform')))
		else:
			addform = AddressForm(request.POST)

		if addform.is_valid():
			try:
				newaddress = addform.save(commit = False)
				newaddress.user = request.user
				newaddress.save()
			except IntegrityError:
				messages.error(request,_('The address already exists!'))
				return render(request, self.template_name, {'addform': addform})

			if add_field_name == 'ship_to_add':
				return render(request, 'main/directshipping.html', {'newaddress': newaddress})
			if add_field_name == 'default_address':
				return render(request, 'main/updateprofile.html', {'newaddress': newaddress})
			else:
				return redirect(reverse('useraddress'))
		else:
			return render(request, self.template_name, {'addform': addform})


class EditAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		addform = AddressForm(instance = add)
		return render(request, self.template_name, {'addform': addform})

	def post(self, request, add_id):

		add = Address.objects.get(pk=add_id)

# never update an address that has been shipped with package(s)
		if Service.objects.filter(ship_to_add=add).count()<1:
			# just update the addresss
			addform = AddressForm(request.POST, instance = add)
		else:
			# create a new addresss
			addform = AddressForm(request.POST)

		if addform.is_valid():
			updateaddress = addform.save(commit = False)
			updateaddress.user = request.user

# when create a new address for update, neet to reset the old one's user to be null
			if addform.instance == None:
				add.user = None
				add.save()

			updateaddress.save()
			return redirect(reverse('useraddress'))
		else:
			return render(request, self.template_name, {'addform': addform})


class DeleteAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		add.user = None
		add.save()

		if add == request.user.default_address:
			user = User.objects.get(user = request.user)
			user.default_address = None
			user.save()
		return redirect(reverse('useraddress'))

class SetDefaultAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		user = User.objects.get(user = request.user)
		user.default_address = add
		user.save()
		return redirect(reverse('useraddress'))



class CollectionPointView(TemplateView):
	template_name = 'main/collectionpoints.html'
	col_list = (CollectionPoint.objects.filter(status=True).
					values('pk', 'name', 'store', 'absent_start', 'absent_end', 'food', 'regular', 'skincare', 'address', 'apt', 'city', 'state', 'country', 'zipcode' ))
	col_json = json.dumps(list(col_list), cls=DjangoJSONEncoder)

	def get(self, request):
		return render(request, self.template_name, {'col_list': self.col_json,})

	def post(self, request):
		print(request.POST.get('selected_col'))
		try:
			col = CollectionPoint.objects.get(pk=request.POST.get('selected_col'))
			if not col.status:
				messages.error(request, _("The Collection Point you select is not avaliable. Please select another one." ))
				return render(request, self.template_name, {'col_list': self.col_json,})
			else:
				return redirect(reverse('add_co_shipping',args = (col.pk,)))
		except:
			messages.error(request, _("Your didn't select a Collection Point yet."))
			return render(request, self.template_name, {'col_list': self.col_json,})



class ShippingView(TemplateView):
	template_name = 'main/select_way_to_ship.html'

	col_list = CollectionPoint.objects.filter(status=True)

	def get(self, request):
		return render(request, self.template_name, {'col_list': self.col_list,})

class WalletView(TemplateView):
	template_name = 'main/wallet.html'

	def get(self, request):
		return render(request, self.template_name)

class ShoppingView(TemplateView):
	template_name = 'main/global_shop.html'

	def get(self, request):
		return render(request, self.template_name)

class InformationView(TemplateView):
	template_name = 'main/information.html'

	def get(self, request, title):
		try:
			information = Resource.objects.get(title=title)
			if information.english_content!='':
				return render(request, self.template_name, {'information': information})
			else:
				return render(request, self.template_name, {'empty': _('Upcoming information')})
		except:
			return render(request, self.template_name, {'empty': _('Upcoming information')})
