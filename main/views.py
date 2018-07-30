from .models import (
	Address, Card, OtherPayMethod, Service, CollectionPoint,
	UserProfile, User, Warehouse, PackageImage, FavoriteWebsite
	)
from .forms import (
	RegisterForm, AddressForm, ItemFormset, PackageForm, UserProfileForm,
	CoShippingForm, DirectShippingForm, ImageFormset, CoReceiverForm, ImageForm, WebFormSet,
	ColResigterForm, ProfileForm
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

from .code import checkAddress


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
		webformset = WebFormSet(request.POST)
		profileform = UserProfileForm(request.POST)

		if form.is_valid() and webformset.is_valid() and profileform.is_valid():
			user = form.save()
			profile = UserProfile.objects.get(user = user)
			profile.phone = profileform.cleaned_data['phone']
			profile.birthday = profileform.cleaned_data['birthday']
			profile.country = profileform.cleaned_data['country'].title()
			profile.language = profileform.cleaned_data['language'].title()
			profile.save()

			for webform in webformset:
				web = webform.save(commit = False)
				web.country = profile.country
				web.web_name = web.web_name.title()

				if webform.is_valid():
					existed_web = FavoriteWebsite.objects.filter(
						web_name = web.web_name,
						web_type = web.web_type,
						country = profile.country)

					if existed_web.count() == 1:
						existed_web = existed_web.first()
						existed_web.rate = existed_web.rate +1
						existed_web.save()
					else:
						web.save()

			if "colregister" in request.POST:
				return redirect(reverse('colregister'))
			else:
				return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {'form': form, 'webformset':webformset, 'profileform':profileform})


class ColRegisterView(TemplateView):
	template_name = 'main/colregister.html'

	def get(self, request):
		colform = ColResigterForm()
		return render(request, self.template_name, {
		 'colform': colform,
		 })

	def post(self, request):
		userform  = ProfileForm(request.POST)
		colform = ColResigterForm(request.POST, request.FILES)
		if colform.is_valid() and userform.is_valid():
			user = User.objects.get(id = request.user.id)

			if user.first_name != userform.cleaned_data['first_name'].title() and user.last_name != userform.cleaned_data['last_name'].title():
# IF THE NAME CHANGED, FOR ALL follow_user_infor ADDRESS OF THIS USER, IF THERE IS ANY PACKAGE SENT TO IT BEFORE,
# CREATE NEW ADDRESS WITH THE SAME INPORMATION AND SET THE OLD ONE USER AS NONE, follow_user_infor = FALSE
				for add in Address.objects.filter(user = user,  follow_user_infor = True):
					checkAddress(add)

				user.first_name = userform.cleaned_data['first_name'].title() or user.first_name
				user.last_name = userform.cleaned_data['last_name'].title() or user.last_name


			if userform.cleaned_data['email'] !='' and userform.cleaned_data['email'] != None:
				user.email = userform.cleaned_data['email'].lower()

			user.save()

			collector = colform.save(commit=False)
			collector.collector = user
			collector.save()

# sst the default_col to the collector
			profile = UserProfile.objects.get(user = user)
			profile.default_col = collector
			profile.phone = userform.cleaned_data['phone']
			profile.birthday = userform.cleaned_data['birthday']
			profile.save()


			return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {
					 'colform': colform,
					 'userform': userform,
					 })

class AccountView(TemplateView):
	template_name = 'main/account.html'

	def get(self, request):
		return render(request, self.template_name)

# >>> article = Article.objects.get(pk=1)
# >>> form = ArticleForm(instance=article)
# >>> a = Article.objects.get(pk=1)
# >>> f = ArticleForm(request.POST, instance=a)
# >>> f.save()


# class LoginView(TemplateView):
# 	template_name = 'main/login.html'
#
# 	def get(self, request):
# 		return render(request, self.template_name)
#
# 	def post(self, request):
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			login(request, user)
# 			return redirect(reverse('home'))
# 		else:
# 			return render(request, self.template_name)
# -----------------------------------------------------------
'''
Update User Profile
'''
# -----------------------------------------------------------
class UpdateProfileView(TemplateView):
	template_name = 'main/updateprofile.html'
	col_list = CollectionPoint.objects.filter(status=True)


	def get(self, request):
		userform  = ProfileForm()
		addform = AddressForm()
		addform.fields['follow_user_infor'].checked = True
		return render(request, self.template_name, {
						'col_list': self.col_list,
						'addform': addform,
						'userform':userform
						})

	def post(self, request):
		userform = ProfileForm(request.POST)
		addform = AddressForm(request.POST)

		if userform.is_valid():
			user = User.objects.get(id = request.user.id)
			profile = UserProfile.objects.get(user = user)

# update the user profile
			try:
	#  save default_address from select
				selected_add = Address.objects.get(pk=request.POST['choice'])
				if profile.default_address != selected_add:
					profile.default_address = selected_add
			except:

	#  save default_address from add new address
				if addform.is_valid():
					newadd = addform.save()
					profile.default_address = newadd
				else:
					return render(request, self.template_name, {
											'col_list': self.col_list,
											'addform': addform,
											'userform':userform
											})

			try:
	#  save default_col from select
				selected_col = CollectionPoint.objects.get(pk=request.POST['col_choice'])
				profile.default_col = selected_col
			except:
				pass

			profile.phone = userform.cleaned_data['phone']
			profile.birthday = userform.cleaned_data['birthday']
			profile.save()

# Update the user account
			if user.first_name != userform.cleaned_data['first_name'].title() and user.last_name != userform.cleaned_data['last_name'].title():
	# IF THE NAME CHANGED, FOR ALL follow_user_infor ADDRESS OF THIS USER, IF THERE IS ANY PACKAGE SENT TO IT BEFORE,
	# CREATE NEW ADDRESS WITH THE SAME INPORMATION AND SET THE OLD ONE USER AS NONE, follow_user_infor = FALSE
				for add in Address.objects.filter(user = user,  follow_user_infor = True):
					checkAddress(add)

				user.first_name = userform.cleaned_data['first_name'].title() or user.first_name
				user.last_name = userform.cleaned_data['last_name'].title() or user.last_name

			if userform.cleaned_data['email'] !='' and userform.cleaned_data['email'] != None:
				user.email = userform.cleaned_data['email'].lower()

			user.save()

			return redirect(reverse('account'), user = user)
		else:
			return render(request, self.template_name, {
									'col_list': self.col_list,
									'addform': addform,
									'userform':userform
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


class AddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request):
		addform = AddressForm()
		addform.fields['follow_user_infor'].required = False
		addform.fields['first_name'].required = False
		addform.fields['last_name'].required = False
		addform.fields['address'].required = False
		addform.fields['city'].required = False
		addform.fields['state'].required = False
		addform.fields['country'].required = False
		addform.fields['zipcode'].required = False
		return render(request, self.template_name, {'addform': addform})


	def post(self, request):
		if "cancel" in request.POST:
			return redirect(reverse('useraddress'))
		else:
			addform = AddressForm(request.POST)
			if addform.is_valid():
				newaddress = addform.save(commit = False)
				newaddress.user = request.user
				newaddress.save()

				return redirect(reverse('useraddress'))

			else:
				return render(request, self.template_name, {'addform': addform})


# Use updateView?

class EditAddressView(TemplateView):
	template_name = 'main/address.html'

	def get(self, request, add_id):
		add = Address.objects.get(pk=add_id)
		addform = AddressForm(instance = add)
		return render(request, self.template_name, {'addform': addform})


	def post(self, request, add_id):
		if "cancel" in request.POST:
			return redirect(reverse('useraddress'))
		else:
			add = Address.objects.get(pk=add_id)

# never update an address that has been shipped with package(s)
			if Service.objects.filter(ship_to_add=add).count()<1:
				addform = AddressForm(request.POST, instance = add)
			else:
				addform = AddressForm(request.POST)

			if addform.is_valid():
				updateaddress = addform.save(commit = False)
				if updateaddress.id != add.id:
					add.user = None
					if add.follow_user_infor:
						add.first_name = request.user.first_name
						add.last_name = request.user.last_name
						add.email = request.user.email
						add.phone = request.user.userprofile.phone
						add.follow_user_infor = False
					add.save()

				return redirect(reverse('useraddress'))

			else:
				return render(request, self.template_name, {'addform': addform})


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
