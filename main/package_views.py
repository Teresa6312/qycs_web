from .models import (
	Address, Service, CollectionPoint, Coupon,
	User, Warehouse, PackageSnapshot, OrderSet
	)
from .forms import (
	ItemFormset, PackageCreationForm, CoShippingCreationForm, DirectShippingCreationForm,
	CoReceiverForm, SnapshotForm, OrderSetForm, CartForm, CoReceiverCheckForm
	)
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponse

from django.urls import reverse
# used to reverse the url name as a url path
from django.utils.translation import gettext as _

from django.shortcuts import render
# from django.core.serializers.json import DjangoJSONEncoder
#
import datetime

class PackagesView(TemplateView):
	template_name = 'main/package_history.html'

	def get(self, request):
		return render(request, self.template_name,
			{'package_list': Service.objects.filter(user = request.user).order_by('-created_date')})


class PackageCartView(TemplateView):
	template_name = 'main/package_cart.html'

	def get(self, request):
		order = OrderSetForm()
		package_list = Service.objects.filter(user = request.user, paid_amount = None).order_by('-created_date')
		return render(request, self.template_name,
			{'package_list': package_list,
			'order':order})

	def post(self, request):
		cart = CartForm(request.user, request.POST)
		if cart.is_valid():
			try:
				coupon = Coupon.objects.get(code = request.POST.get('coupon'))
			except:
				coupon = None

			orderSet = OrderSet(coupon = coupon, total_amount = 0.0)
			orderSet.save()

			amount = 0;
			for pack in cart.cleaned_data['package_set']:
				package = Service.objects.get(id = pack.id )
				if package.get_total()>0:
					package.order_set = orderSet
					package.save()
					amount = package.get_total() + amount

			orderSet.total_amount = amount
			orderSet.currency = orderSet.service_set.first().currency
			orderSet.save()
			request.session['order_set_id'] = orderSet.id
			return redirect(reverse('payment:process'))
		else:
			return redirect(reverse('packagecart'))

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
			paid_amount = None).order_by('-id')

		return render(request, self.template_name,
				{'form': form,
				'package_list': package_list,
				'itemset': itemset,
				})


	def post(self, request):
		form = DirectShippingCreationForm(request.POST)
		form.fields['ship_to_add'].required = True
		itemset = ItemFormset(request.POST)
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = False,
			paid_amount = None).order_by('-id')

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

			if "finish" in request.POST:
				return redirect(reverse('packagecart'))
			else:
				messages.info(request,_(package.cust_tracking_num + ' is created successfully!'))
				return redirect(reverse('add_direct_shipping'))
		else:

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
		today = datetime.datetime.now()
		try:
			 last_created = Service.objects.filter(user = request.user,co_shipping = True).latest('created_date')
			 receiverform = CoReceiverForm(receiver = last_created.receiver)
		except:
			receiverform = CoReceiverForm()
		form = CoShippingCreationForm()
		itemset = ItemFormset()
		try:
			col = CollectionPoint.objects.get(pk=selected_col)
			if col.status:
				package_list = Service.objects.filter(
					user = request.user,
					co_shipping = True,
					paid_amount = None).order_by('-id')

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
		col = CollectionPoint.objects.get(pk=selected_col)
		form = CoShippingCreationForm(request.POST)
		itemset = ItemFormset(request.POST)
		receiverform = CoReceiverCheckForm(request.POST)
		package_list = Service.objects.filter(
			user = request.user,
			co_shipping = True,
			paid_amount = None).order_by('-id')

		if form.is_valid() and itemset.is_valid() and receiverform.is_valid():
			files = self.request.FILES.getlist('image')
			package = form.save(commit = False)

			package.co_shipping = True
			package.ship_to_col = col
			package.receiver = receiverform.check()
			package.user = request.user

			package.save()

			itemset.instance = package
			itemset.save()

	# how to make it more secury
			for f in files:
				newimage = PackageSnapshot(package = package, snapshot = f)
				newimage.save()

			if "finish" in request.POST:
				return redirect(reverse('packagecart'))
			else:
				messages.info(request,_(package.cust_tracking_num + ' is created successfully!'))
				return redirect(reverse('add_co_shipping',args = (selected_col,)))
		else:
			return render(request, self.template_name, {
													'form': form,
													'receiverform':receiverform,
													'package_list': package_list,
													'itemset': itemset,
													'selected_col': col,
													})


class PackageDetailView(TemplateView):
	template_name = 'main/package_detail.html'

	def get(self, request, pack_id):
		try:
			package = Service.objects.get(pk=pack_id,user=request.user)
			return render(request, self.template_name , {'package': package})
		except ObjectDoesNotExist:
			messages.error(request, _("Cannot Find the package"))
			# return render(request,reverse('userpackages'))


def couponView(request):
	if request.POST:
		code=request.POST.get('coupon','')
		try:
			coupon = Coupon.objects.get(code = code)
			return HttpResponse(coupon.discount)
		except:
			return HttpResponse()
