from .models import (
	Address, Card, OtherPayMethod, Service, CollectionPoint,
	UserProfile, User, Warehouse, PackageImage, FavoriteWebsite
	)
from .forms import (
	RegisterForm, ProfileUpdateForm, AddressForm, ItemFormset, PackageForm, UserProfileForm,
	CoShippingForm, DirectShippingForm, ImageFormset, CoReceiverForm, ImageForm, WebFormSet,
	ColResigterForm
	)
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from .code import checkAddress
from django.urls import reverse
# used to reverse the url name as a url path


class HomeView(TemplateView):
	template_name = 'main/home.html'

	def get(self, request):
		return render(request, self.template_name)


class RegisterView(TemplateView):
	template_name = 'main/register.html'

	def get(self, request):
		form = RegisterForm()
		webformset = WebFormSet()
		profileform = UserProfileForm()
		return render(request, self.template_name, {'form': form, 'webformset':webformset, 'profileform':profileform})

	def post(self, request):
		form = RegisterForm(request.POST)

		if form.is_valid():
			user = form.save()
			webformset = WebFormSet(request.POST)
			profileform = UserProfileForm(request.POST)

			# if webformset.is_valid():
				# web = FavoriteWebsite.objects.get(web_name = webform.cleaned_data['web_name'], country = webform.cleaned_data['country'])
				# if web.count() == 1:
				# 	web.rate = web.rate +1
				# 	web.save()
				# else:
				# 	webform.save()

			if profileform.is_valid():
				profile = UserProfile.objects.get(user = user)
				profile.phone = profileform.cleaned_data['phone']
				profile.birthday = profileform.cleaned_data['birthday']
				profile.country = profileform.cleaned_data['country']
				profile.language = profileform.cleaned_data['language']
				profile.save()
			if "colregister" in request.POST:
				return redirect(reverse('colregister'))
			else:
				return redirect(request, reverse('account'))
		else:
			return render(request, self.template_name, {'form': form})


class ColRegisterView(TemplateView):
	template_name = 'main/colregister.html'

	def get(self, request):
		colform = ColResigterForm()
		return render(request, self.template_name, {
		 'colform': colform,
		 })

	def post(self, request):
		colform = ColResigterForm(request.POST)

		if colform.is_valid():
			user = User.objects.get(user = request.user)
			collector = CollectionPoint.objects.get(collector = user)
			collector.name = colform.cleaned_data['name']
			collector.license = colform.cleaned_data['license']
			collector.license_type = colform.cleaned_data['license_type']
			collector.store = colform.cleaned_data['store']
			# save image then save instance
			# collector.id_image
			# collector.license_image
			# collector.image
			# collector.save()

			return redirect(request, reverse('account'))
		else:
			return render(request, self.template_name, {'colform': colform})


class AccountView(TemplateView):
	template_name = 'main/account.html'

	def get(self, request):
		return render(request, self.template_name)


class LoginView(TemplateView):
	template_name = 'main/login.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			print('----------------------------------------')
			print(request.path_info)
			return redirect(reverse('home'))
		else:
			return render(request, self.template_name)
# -----------------------------------------------------------
'''
Update User Profile
'''
# -----------------------------------------------------------
class UpdateProfileView(TemplateView):
	template_name = 'main/updateprofile.html'

	def get(self, request):
		col_list = CollectionPoint.objects.filter(status=True)
		return render(request, self.template_name, {'col_list':col_list})

	def post(self, request):
		form = ProfileUpdateForm(request.POST)
		if form.is_valid():
			profile = UserProfile.objects.get(user = request.user)
			try:
				selected_add = Address.objects.get(pk=request.POST['choice'])
				if profile.default_address != selected_add:
					profile.default_address = selected_add
					profile.save()

					form.cleaned_data['address']=''
			except:
				pass

			try:
				selected_col = CollectionPoint.objects.get(pk=request.POST['col_choice'])
				profile.default_col = selected_col
				profile.save()
			except:
				pass

			user = form.save(request.user)

			return redirect(reverse('account'), user = user)
		else:
			messages.info(request, 'Invalid address, please try again!')
			return render(request, self.template_name, {'form':form})




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


class AddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request):
		form = AddressForm()
		return render(request, self.template_name, {'form': form})


	def post(self, request):
		if "cancel" in request.POST:
			return redirect(reverse('useraddress'))
		else:
			form = AddressForm(request.POST)
			if form.is_valid():
				newaddress = form.save(commit = False)

				if newaddress.address != None and newaddress.address != '':
					newaddress.user = request.user
					newaddress.save()

				return redirect(reverse('useraddress'))

			else:
				messages.info(request, 'Invalid address, please try again!')
				return render(request, self.template_name, {'form': form})


# Use updateView?

class EditAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		form = AddressForm()
		add = Address.objects.get(pk=add_id)
		return render(request, self.template_name, {'form': form, 'add':add})


	def post(self, request, add_id):
		if "cancel" in request.POST:
			return redirect(reverse('useraddress'))
		else:
			form = AddressForm(request.POST)

			add = Address.objects.get(pk=add_id)

			if form.is_valid():
				newaddress = form.save(commit = False)
				if Service.objects.filter(ship_to_add=add).count()>=1:
					newaddress.user = request.user
					newaddress.save()

					if add.follow_user_infor:
						add.first_name = request.user.first_name
						add.last_name = request.user.last_name
						add.email = request.user.email
						add.phone = request.user.userprofile.phone
						add.follow_user_infor = False
					add.user = None
				else:
					add.first_name = newaddress.first_name
					add.last_name = newaddress.last_name
					add.follow_user_infor = newaddress.follow_user_infor
					add.address = newaddress.address
					add.apt = newaddress.apt
					add.city = newaddress.city
					add.country = newaddress.country
					add.state = newaddress.state
					add.zipcode = newaddress.zipcode
					add.email = newaddress.email
					add.phone = newaddress.phone

				add.save()

				return redirect(reverse('useraddress'))

			else:
				form = AddressForm(request.POST)
				messages.info(request, 'Invalid address, please try again!')
				return render(request, self.template_name, {'form': form})


class DeleteAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)

		if add.follow_user_infor:
			add.first_name = request.user.first_name
			add.last_name = request.user.last_name
			add.email = request.user.email
			add.phone = request.user.userprofile.phone
			add.follow_user_infor = False
		add.user = None
		add.save()

		if add == request.user.userprofile.default_address:
			profile = UserProfile.objects.get(user = request.user)
			profile.default_address = None
			profile.save()
		return redirect(reverse('useraddress'))

class SetDefaultAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		profile = UserProfile.objects.get(user = request.user)
		profile.default_address = add
		profile.save()
		return redirect(reverse('useraddress'))


class WalletView(TemplateView):
	template_name = 'main/wallet.html'

	def get(self, request):
		cards = Card.objects.filter(user = request.user)
		paypals = OtherPayMethod.objects.filter(user = request.user, method = 'Paypal')
		wechats = OtherPayMethod.objects.filter(user = request.user, method = 'WeChat')
		alipays = OtherPayMethod.objects.filter(user = request.user, method = 'Alipays')

		return render(request, self.template_name ,
			 {'cards': cards,
				'paypals':paypals,
				'wechats' :wechats,
				'alipay': alipays,
			 })


class CollectionPointView(TemplateView):
	template_name = 'main/collectionpoints.html'
	col_list = CollectionPoint.objects.filter(status=True)

	def get(self, request):

		return render(request, self.template_name, {'col_list': self.col_list,})

	def post(self, request):
		try:
			selected_col = CollectionPoint.objects.get(pk=request.POST['choice'])

			return redirect(reverse('add_co_shipping',args = (selected_col.pk,)))

		except (KeyError, CollectionPoint.DoesNotExist):
			# Redisplay the question voting form.
			return render(request, self.template_name, {
				'col_list': self.col_list,
				'error_message': "You didn't select a Collection Point.",
			})
