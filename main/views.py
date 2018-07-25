from .models import (
	Address, Card, OtherPayMethod, Service, CollectionPoint,
	UserProfile, User, Warehouse, PackageImage, FavoriteWebsite
	)
from .forms import (
	RegisterForm, ProfileUpdateForm, AddressForm, ItemFormset, PackageForm, UserProfileForm,
	CoShippingForm, DirectShippingForm, ImageFormset, CoReceiverForm, ImageForm, WebFormSet
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

			return redirect(request, reverse('account'))
		else:
			return render(request, self.template_name, {'form': form})


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
		form = AddressForm(request.POST)
		if form.is_valid():
			newaddress = form.save(commit = False)

			if newaddress.address != None and newaddress.address != '':
				newaddress.user = request.user
				newaddress.save()

			return redirect(reverse('useraddress'))

		else:
			form = AddressForm(request.POST)
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



class PackagesView(TemplateView):
	template_name = 'main/packagelist.html'

	def get(self, request):
		return render(request, self.template_name,
			{'package_list': Service.objects.filter(user = request.user).order_by('-created_date')})


class PackageCardView(TemplateView):
	template_name = 'main/packagecar.html'

	def get(self, request):
		return render(request, self.template_name,
			{'package_list': Service.objects.filter(user = request.user, paid_key = None)})



#-----------------------------------------------------------------------------------------
'''
Create Package
'''
#-----------------------------------------------------------------------------------------
class AddPackageView(FormView):
	form_class = CoShippingForm
	template_name = 'main/coshipping.html'
	success_url = '/'

	def get_context_data(self, **kwargs):

		data = super(AddPackageView, self).get_context_data(**kwargs)

		print('-----------------------------------------')
		print(self.get_success_url())

		data['imageset'] = ImageForm()
		data['package_list'] = Service.objects.filter(
			user = self.request.user,
			co_shipping = None,
			paid_key = None).order_by('-id')

		if self.request.POST:
			data['itemset'] = ItemFormset(self.request.POST)
			data['receiver'] = CoReceiverForm(self.request.POST)
			# data['selected_col'] = CollectionPoint.objects.get(pk=self.url.selected_col)
		else:
			data['itemset'] = ItemFormset()
			data['receiver'] = CoReceiverForm()

			# data['selected_col'] = CollectionPoint.objects.get(pk=self.url.selected_col)
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		items = context['itemset']
		images = context['imageset']
		receiver = context['receiver']
		files = self.request.FILES.getlist('image')
		# col = context['selected_col']
		with transaction.atomic():
			receiver = receiver.save(self.request.user)

			self.object = form.save(commit=False)
			self.object.user = User.objects.get(pk = self.request.user.id)
			self.object.wh_received = Warehouse.objects.get(pk=1)
			self.object.co_shipping = None
			self.object.receiver = receiver
			# self.object.ship_to_col = col
			self.object.save()


			if items.is_valid():
				items.instance = self.object
				items.save()
			# if images.is_valid():
			print("----------------image----------")
			print(files)
			for f in files:
				newimage = PackageImage(package = self.object, image = f)
				newimage.save()

		return super(AddPackageView, self).form_valid(form)






#-----------------------------------------------------------------------------------------
'''
Create Direct Shipping Package
'''
#-----------------------------------------------------------------------------------------

class AddDirectShipping(FormView):
	form_class = DirectShippingForm
	template_name = 'main/directshipping.html'
	success_url = '/packages/direct-shipping/add'

	def get_context_data(self, **kwargs):
		data = super(AddDirectShipping, self).get_context_data(**kwargs)
		data['imageset'] = ImageForm()
		data['package_list'] = Service.objects.filter(
			user = self.request.user,
			co_shipping = False,
			paid_key = None).order_by('-id')

		if self.request.POST:
			data['itemset'] = ItemFormset(self.request.POST)
			data['new_address'] = AddressForm(self.request.POST)
			data['add_id'] = self.request.POST['choice']
		else:
			data['itemset'] = ItemFormset()
			data['new_address'] = AddressForm()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		items = context['itemset']
		images = context['imageset']
		if context['add_id'] != None and context['add_id'] !='':
			address = Address.objects.get(pk=context['add_id'])
		elif context['new_address'] != None and context['new_address']:
			address = context['new_address']
			if address.is_valid():
				address.save()

		files = self.request.FILES.getlist('image')

		with transaction.atomic():

			self.object = form.save(commit=False)
			self.object.user = User.objects.get(pk = self.request.user.id)
			self.object.wh_received = Warehouse.objects.get(pk=1)
			self.object.co_shipping = False
			print("------------------------------------------")
			print(address)
			self.object.ship_to_add = address or Address.objects.get(pk=self.cleaned_data['ship_to_add'])
			self.object.save()

			if items.is_valid():
				items.instance = self.object
				items.save()


# Does it save to just save the image directly?
			for f in files:
				newimage = PackageImage(package = self.object, image = f)
				newimage.save()

		return super(AddDirectShipping, self).form_valid(form)


#-----------------------------------------------------------------------------------------
'''
Create Co-shipping Package
'''
#-----------------------------------------------------------------------------------------
class SetPickupPointView(TemplateView):
	template_name = 'main/collectionpoints.html'
	# col_list = CollectionPoint.objects.filter(status=True)
	col_list = CollectionPoint.objects.all()

	def get(self, request):

		return render(request, self.template_name, {'col_list': self.col_list,})

	def post(self, request):
		try:
			selected_col = CollectionPoint.objects.get(pk=request.POST['choice'])

			if selected_col.status:
				return redirect(reverse('add_co_shipping',args = (selected_col.pk,)))
			else:
				return render(request, self.template_name, {
				'col_list': self.col_list,
				'error_message': "You didn't select a Collection Point.",
				})

		except (KeyError, CollectionPoint.DoesNotExist):
			# Redisplay the question voting form.
			return render(request, self.template_name, {
				'col_list': self.col_list,
				'error_message': "You didn't select a Collection Point.",
			})





class AddCoShipping(TemplateView):
	template_name = 'main/coshipping.html'


	def get(self, request, selected_col):
		form = CoShippingForm()
		itemset = ItemFormset()
		imageset = ImageFormset()
		receiverform = CoReceiverForm()
		try:
			col = CollectionPoint.objects.get(pk=selected_col)
			if col.status:
				package_list = Service.objects.filter(
					user = request.user,
					co_shipping = True,
					paid_key = None).order_by('-id')

				return render(request, self.template_name,
					{'form': form,
					'receiverform':receiverform,
					'package_list': package_list,
					'itemset': itemset,
					'imageset': imageset,
					'selected_col': col,
					})
			else:
				return redirect(reverse('collection_points'))
		except:
			return redirect(reverse('collection_points'))




	def post(self, request, selected_col):
		form = CoShippingForm(request.POST)
		receiverform = CoReceiverForm(request.POST)
		itemset = ItemFormset(request.POST)
		imageset = ImageFormset(request.POST)

		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = True,
			paid_key = None).order_by('-id')

		col = CollectionPoint.objects.get(pk=selected_col)


		if form.is_valid and receiverform.is_valid():

			package = form.save(commit = False)

			with transaction.atomic():

				package.co_shipping = True
				# default warehouse is China
				package.wh_received = Warehouse.objects.get(pk=1)
				package.ship_to_col = col
				package.user = User.objects.get(pk = request.user.id)


				receiver = receiverform.save(request.user)
				package.receiver = receiver
				package = package.save()


				if itemset.is_valid():
					itemset.instance = package
# no id................??????????????
					itemset.save()

					print("--------------itemset---------------")
					print(itemset)
				if imageset.is_valid():
					imageset.instance = package
					imageset.save()

					print("--------------imageset---------------")
					print(imageset.image)

			return redirect(reverse('add_co_shipping',args = (selected_col,)))
		else:
			messages.info(request, 'Invalid form!')

			return render(request, self.template_name,
			{'form': self.form,
			'receiverform':self.receiverform,
			'package_list': package_list,
			'itemset': self.itemset,
			'imageset': self.imageset,
			'selected_col': col,
			})






class PackageAddedView(TemplateView):
	template_name = 'main/packageadded.html'

	def post(self, request):
		form = PackageForm(request.POST)
		if form.is_valid():
			newpackage = form.save(commit = False)
			newpackage.user = request.user
			carrier = newpackage.cust_carrier
			tracking_num = newpackage.cust_tracking_num
			package = Service.objects.filter(cust_carrier = carrier, cust_tracking_num = tracking_num)
			if len(package) == 0 or package == None:
				newpackage.save()
			else:
				messages.info(request, 'You have add this package before!')

			return render(request, self.template_name , {'tracking_num': tracking_num})
			# why it didn't return to get?
		else:
			messages.info(request, 'Invalid form!')

			# return render(request, 'main/addpackage.html' , {'form': form})
			return redirect(reverse('userpackages'))
