from .models import (
	Address, Service, CollectionPoint,
	UserProfile, User, Warehouse, PackageImage, FavoriteWebsite
	)
from .forms import (
	AddressForm, ItemFormset, PackageForm,
	CoShippingForm, DirectShippingForm, ImageFormset, CoReceiverForm, ImageForm
	)
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django.urls import reverse
# used to reverse the url name as a url path


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
	form_class = PackageForm
	template_name = 'main/addpackage_old.html'
	success_url = '/package/add'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['imageset'] = ImageForm()
		data['package_list'] = Service.objects.filter(
			user = self.request.user,
			co_shipping = None,
			paid_key = None).order_by('-id')

		if self.request.POST:
			data['itemset'] = ItemFormset(self.request.POST)
		else:
			data['itemset'] = ItemFormset()

		return data

	def form_valid(self, form):
		context = self.get_context_data()
		items = context['itemset']
		images = context['imageset']
		files = self.request.FILES.getlist('image')
		with transaction.atomic():

			self.object = form.save(commit=False)
			self.object.user = User.objects.get(pk = self.request.user.id)
			self.object.wh_received = Warehouse.objects.get(pk=1)
			self.object.co_shipping = None
			self.object.save()


			if items.is_valid():
				items.instance = self.object
				items.save()
# if images.is_valid():

			for f in files:
				newimage = PackageImage(package = self.object, image = f)
				newimage.save()

		return super().form_valid(form)






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




class AddCoShipping(TemplateView):
	template_name = 'main/coshipping.html'


	def get(self, request, selected_col):
		form = CoShippingForm()
		itemset = ItemFormset()
		imageset = ImageForm()
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
		imageset = ImageForm(request.POST)
		files = self.request.FILES.getlist('image')
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = True,
			paid_key = None).order_by('-id')

		col = CollectionPoint.objects.get(pk=selected_col)


		if form.is_valid() and receiverform.is_valid():

			package = form.save(commit = False)

			with transaction.atomic():

				package.co_shipping = True
# default warehouse is China
				package.wh_received = Warehouse.objects.get(pk=1)
				package.ship_to_col = col
				package.user = User.objects.get(pk = request.user.id)


				receiver = receiverform.save(request.user)
				package.receiver = receiver
				package.save()


				if itemset.is_valid():
					itemset.instance = package
					itemset.save()
# how to make it more secury
				for f in files:
					newimage = PackageImage(package = package, image = f)
					newimage.save()

			return redirect(reverse('add_co_shipping',args = (selected_col,)))
		else:
			messages.info(request, 'Invalid form!')

			return render(request, self.template_name,
			{'form': form,
			'receiverform':receiverform,
			'package_list': package_list,
			'itemset': itemset,
			'imageset': imageset,
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
