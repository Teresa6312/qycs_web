from .models import (
	Address, Service, CollectionPoint, Coupon, ParentPackage,
	User, Warehouse, PackageSnapshot, OrderSet
	)
from .forms import (
	ItemFormset, PackageCreationForm, CoShippingCreationForm, DirectShippingCreationForm,
	CoReceiverForm, SnapshotForm, OrderSetForm, CartForm, CoReceiverCheckForm, PackageChangeForm
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
from django.http import HttpResponseRedirect
# from django.core.serializers.json import DjangoJSONEncoder
#
import datetime
import json

class PackagesView(TemplateView):
	template_name = 'main/package_history.html'

	def get(self, request):
		order_list = Service.objects.filter(user = request.user, order = True).exclude(paid_amount=None).order_by('-created_date')
		co_shipping_list = Service.objects.filter(user = request.user, order = False, co_shipping = True).exclude(paid_amount=None).order_by('-created_date')
		parent_package_list = ParentPackage.objects.filter(service__user = request.user, service__co_shipping = False, service__order = False).exclude(paid_amount=None).distinct().order_by('-created_date')

		return render(request, self.template_name,
			{'order_list': order_list,
			'co_shipping_list': co_shipping_list,
			'parent_package_list': parent_package_list})


def ReturnPackageNumber(request):
	packageNumber=Service.objects.filter(user = request.user, paid_amount = None).order_by('-created_date').count()
	return HttpResponse(packageNumber)

class PackageCartView(TemplateView):
	template_name = 'main/package_cart.html'

	def get(self, request):
		order = OrderSetForm()
		order_list = Service.objects.filter(user = request.user, paid_amount = None, order = True).order_by('created_date')
		co_shipping_list = Service.objects.filter(user = request.user, paid_amount = None, order = False, co_shipping = True).order_by('created_date')
		direct_shipping_list = Service.objects.filter(user = request.user, paid_amount = None, order = False, co_shipping = False, parent_package = None).order_by('created_date')
		parent_package_list = ParentPackage.objects.filter(service__user = request.user, service__co_shipping = False, service__order = False, service__paid_amount = None).distinct().order_by('created_date')


		return render(request, self.template_name,
			{'order_list': order_list,
			'co_shipping_list': co_shipping_list,
			'direct_shipping_list': direct_shipping_list,
			'parent_package_list': parent_package_list,
			'order':order})

	def post(self, request):
		cart = CartForm(request.user, request.POST)
		order = OrderSetForm(request.POST)
		if cart.is_valid() and order.is_valid():
			if cart.cleaned_data['package_set'] or cart.cleaned_data['parent_package_set']:
				try:
					coupon = Coupon.objects.get(code = request.POST.get('code'))
				except:
					coupon = None

				orderSet = order.save()
				orderSet.coupon = coupon

				amount = 0;
				for pack in cart.cleaned_data['package_set']:
					package = Service.objects.get(id = pack.id )
					if package.get_total()>0:
						package.order_set = orderSet
						package.save()
						amount = package.get_total() + amount


				for parent_pack in cart.cleaned_data['parent_package_set']:
					package = ParentPackage.objects.get(id = parent_pack.id )
					if float (package.package_amount)>0:
						package.order_set = orderSet
						package.save()
						amount = float (package.package_amount) + amount

				orderSet.total_amount = amount
				if orderSet.service_set.all():
					orderSet.currency = orderSet.service_set.first().currency
				else:
					orderSet.currency = orderSet.parentpackage_set.first().currency
				orderSet.save()
				request.session['order_set_id'] = orderSet.id

				return redirect(reverse('payment:process'))
			else:
				return redirect(reverse('packagecart'))
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
				messages.error(request,_('The Collection Point you selected is not available right now! Please choose another one.'))
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
			if not request.user.default_col:
				user = User.objects.get(id = request.user.id)
				user.default_col = col
				user.save()

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
			package = Service.objects.get(pk=pack_id)
			if package.user == request.user:
				return render(request, self.template_name , {'package': package})
			else:
				messages.error(request, _(package.cust_tracking_num + " is not your package. You cannot view the detail."))
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		except ObjectDoesNotExist:
			messages.error(request, _("Cannot Find the package"))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PackageChangeView(TemplateView):
	template_name = 'main/package_change.html'

	def get(self, request, pack_id):
		try:
			package = Service.objects.get(pk=pack_id)
			if package.user == request.user:
				form = PackageChangeForm(instance=package)
				return render(request, self.template_name , {'form': form})
			else:
				messages.error(request, _(package.cust_tracking_num + " is not your package. You cannot view the detail."))
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		except ObjectDoesNotExist:
			messages.error(request, _("Cannot Find the package"))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def couponView(request):
	if request.POST:
		code=request.POST.get('coupon','')
		try:
			coupon = Coupon.objects.get(code = code)
			if coupon.check_coupon:
				context = json.dumps({
				'amount_limit': coupon.amount_limit,
				'package': coupon.package,
				'order': coupon.order,
				'discount': coupon.discount,
				})
				return HttpResponse(context)
			else:
				return HttpResponse(False)
		except:
			return HttpResponse()


class ConfirmDirectShipping(TemplateView):
		template_name = 'main/confirm_direct_shipping.html'

		def get(self, request):
			order = OrderSetForm()
			package_list = Service.objects.filter(user = request.user, paid_amount = None, order = False, co_shipping = False, parent_package = None).order_by('-created_date')
			return render(request, self.template_name,
				{'package_list': package_list,
				'order':order})

		def post(self, request):
			cart = CartForm(request.user, request.POST)
			if cart.is_valid():
				parent_pack = ParentPackage()
				parent_pack.save()

				for pack in cart.cleaned_data['package_set']:
					package = Service.objects.get(id = pack.id )
					if package.issue == '':
						package.parent_package = parent_pack
						package.save()

				return redirect(reverse('packagecart'))
			else:
				return redirect(reverse('confirm_direct_shipping'))
