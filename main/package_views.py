from .models import (
	Address, Service, CollectionPoint,
	User, Warehouse, PackageSnapshot
	)
from .forms import (
	ItemFormset, PackageCreationForm, CoShippingCreationForm, DirectShippingCreationForm, CoReceiverForm, SnapshotForm
	)
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django.urls import reverse
# used to reverse the url name as a url path
from django.utils.translation import gettext as _

class PackagesView(TemplateView):
	template_name = 'main/package_history.html'

	def get(self, request):
		return render(request, self.template_name,
			{'package_list': Service.objects.filter(user = request.user).order_by('-created_date')})


class PackageCartView(TemplateView):
	template_name = 'main/package_cart.html'

	def get(self, request):
		return render(request, self.template_name,
			{'package_list': Service.objects.filter(user = request.user, paid_key = None).order_by('-created_date')})

#
# #-----------------------------------------------------------------------------------------
# '''
# Create Package
# '''
# #-----------------------------------------------------------------------------------------
# class AddPackageView(FormView):
# 	form_class = PackageCreationForm
# 	template_name = 'main/addpackage.html'
# 	success_url = '/package/add'
#
# 	def get_context_data(self, **kwargs):
# 		data = super().get_context_data(**kwargs)
# 		data['imageset'] = SnapshotForm()
# 		data['package_list'] = Service.objects.filter(
# 			user = self.request.user,
# 			co_shipping = None,
# 			paid_key = None).order_by('-id')
#
# 		if self.request.POST:
# 			data['itemset'] = ItemFormset(self.request.POST)
# 		else:
# 			data['itemset'] = ItemFormset()
# 		return data
#
# 	def form_valid(self, form):
# 		context = self.get_context_data()
# 		items = context['itemset']
# 		images = context['imageset']
# 		files = self.request.FILES.getlist('image')
# 		with transaction.atomic():
#
# 			self.object = form.save(commit=False)
# 			self.object.user = User.objects.get(pk = self.request.user.id)
# 			self.object.wh_received = Warehouse.objects.get(pk=1)
# 			self.object.co_shipping = None
# 			self.object.save()
#
#
# 			if items.is_valid():
# 				items.instance = self.object
# 				items.save()
# # if images.is_valid():
#
# 			for f in files:
# 				newimage = PackageImage(package = self.object, image = f)
# 				newimage.save()
#
# 		return super().form_valid(form)
#
#




#-----------------------------------------------------------------------------------------
'''
Create Direct Shipping Package
'''
#-----------------------------------------------------------------------------------------

class AddDirectShipping(TemplateView):
	template_name = 'main/directshipping.html'

	def get(self, request):
		form = DirectShippingCreationForm()
		itemset = ItemFormset()
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = False,
			paid_key = None).order_by('-id')

		return render(request, self.template_name,
				{'form': form,
				'package_list': package_list,
				'itemset': itemset,
				})


	def post(self, request):
		form = DirectShippingCreationForm(request.POST)
		itemset = ItemFormset(request.POST)
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = False,
			paid_key = None).order_by('-id')

# 		try:
# #  save default_address from select
# 			selected_add = Address.objects.get(pk=request.POST['selected_add'])
# 		except:
# 			messages.error(request, _('There is some error in your address, please select again!'))
			# return render(request, self.template_name,
			# 			{'form': form,
			# 			'package_list': package_list,
			# 			'itemset': itemset,
			# 			})

		if form.is_valid() and itemset.is_valid():
			files = self.request.FILES.getlist('image')
			package = form.save(commit = False)

			package.co_shipping = False

			package.user = request.user

			package.save()

			itemset.instance = package
			itemset.save()

# how to make it more secury
			for f in files:
				newimage = PackageSnapshot(package = package, snapshot = f)
				newimage.save()

			return redirect(reverse('add_direct_shipping'))
		else:

			messages.error(request, _('Invalid form!'))
			return render(request, self.template_name,
						{'form': form,
						'package_list': package_list,
						'itemset': itemset,
						})


#-----------------------------------------------------------------------------------------
'''
Create Co-shipping Package
'''
#-----------------------------------------------------------------------------------------

class AddCoShipping(TemplateView):
	template_name = 'main/coshipping.html'


	def get(self, request, selected_col):
		form = CoShippingCreationForm()
		receiverform = CoReceiverForm()
		itemset = ItemFormset()
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
					'selected_col': col,
					'itemset':itemset,
					})
			else:
				messages.error(request,_('The Collection Point you selected is not avaliable right now! Please choose another one.'))
				return redirect(reverse('collection_points'))
		except:
			return redirect(reverse('collection_points'))


	def post(self, request, selected_col):
		form = CoShippingCreationForm(request.POST)
		receiverform = CoReceiverForm(request.POST)
		try:
			itemset = ItemFormset(request.POST)
		except:
			itemset = None
		try:
			imageset = ImageForm(request.POST)
		except:
			imageset = None
		files = self.request.FILES.getlist('image')
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = True,
			paid_key = None).order_by('-id')

		col = CollectionPoint.objects.get(pk=selected_col)


		if form.is_valid() and receiverform.is_valid():

			package = form.save(commit = False)
			package.co_shipping = True
# default warehouse is China
			package.wh_received = Warehouse.objects.get(pk=1)
			package.ship_to_col = col
			package.user = request.user


			receiver = receiverform.save()
			package.receiver = receiver
			package.save()

			if itemset != None:
				if itemset.is_valid():
					itemset.instance = package
					itemset.save()

# how to make it more secury
			for f in files:
				newimage = PackageSnapshot(package = package, snapshot = f)
				newimage.save()

			return redirect(reverse('add_co_shipping',args = (selected_col,)))
		else:
			messages.error(request, 'Invalid form!')

			return render(request, self.template_name,
			{'form': form,
			'receiverform':receiverform,
			'package_list': package_list,
			'itemset': itemset,
			'imageset': imageset,
			'selected_col': col,
			})


class PackageDetailView(TemplateView):
	template_name = 'main/package_detail.html'

	def get(self, request, pack_id):
		try:
			package = Service.objects.get(pk=pack_id)
			return render(request, self.template_name , {'package': package})
		except ObjectDoesNotExist:
			messages.error(request, _("Cannot Find the package"))
			return render(request,reverse('userpackages'))
