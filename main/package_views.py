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
from django.core.exceptions import ObjectDoesNotExist

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
	template_name = 'main/packagecard.html'

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
	template_name = 'main/addpackage.html'
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
	template_name = 'main/directshipping.html'

	def get(self, request):
		form = DirectShippingForm()
		itemset = ItemFormset()
		imageset = ImageForm()

		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = False,
			paid_key = None).order_by('-id')

		return render(request, self.template_name,
				{'form': form,
				'package_list': package_list,
				'itemset': itemset,
				'imageset': imageset,
				})



	def post(self, request):
		form = DirectShippingForm(request.POST)
		itemset = ItemFormset(request.POST)
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = False,
			paid_key = None).order_by('-id')
		try:
#  save default_address from select
			selected_add = Address.objects.get(pk=request.POST['selected_add'])
		except:
			messages.info(request, 'Cannot find your address, please try again!')

			return render(request, self.template_name,
						{'form': form,
						'package_list': package_list,
						'itemset': itemset,
						'imageset': imageset,
						})

		if form.is_valid() and itemset.is_valid():
			files = self.request.FILES.getlist('image')
			package = form.save(commit = False)

			with transaction.atomic():

				package.co_shipping = False
# default warehouse is China
				package.wh_received = Warehouse.objects.get(country='China')
				package.ship_to_add = selected_add
				package.user = User.objects.get(pk = request.user.id)

				package.save()

				itemset.instance = package
				itemset.save()

# how to make it more secury
				for f in files:
					newimage = PackageImage(package = package, image = f)
					newimage.save()

			return redirect(reverse('add_direct_shipping'))
		else:
			messages.info(request, 'Invalid form!')
			return render(request, self.template_name,
						{'form': form,
						'package_list': package_list,
						'itemset': itemset,
						'imageset': imageset,
						})


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



class PackageDetailView(TemplateView):
	template_name = 'main/package_detail.html'

	def get(self, request, pack_id):
		try:
			package = Service.objects.get(pk=pack_id)
			return render(request, self.template_name , {'package': package})
		except ObjectDoesNotExist:
			messages.error(request, "Cannot Find the package")
			return render(request,reverse('userpackages'))
