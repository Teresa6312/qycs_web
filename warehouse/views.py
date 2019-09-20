from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from main.models import Service, PriceRate, ParentPackage
from main.forms import TrackingForm
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CoPriceCalForm, EnterVolumeForm, IssueForm, PriceCalForm
from django.urls import reverse
import math
from datetime import date
from django.contrib import messages
from django.utils.translation import gettext as _
from main.code import send_copackage_ready_to_pay_email, send_package_ready_to_pay_email

class HomeView(TemplateView):
	template_name = 'warehouse/home.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			not_ready_co_pack_num = Service.objects.filter(paid_amount=None, co_shipping = True).count()
			not_ready_pack_num = Service.objects.filter(parent_package__paid_amount=None, co_shipping = False).count()
			ready_co_pack_num =  Service.objects.filter(co_shipping = True, parent_package__shipped_date = None).exclude(paid_amount=None).count()
			ready_pack_num =  Service.objects.filter(co_shipping = False, parent_package__shipped_date = None).exclude(parent_package__paid_amount=None).count()
			shipped_co_pack_num =  Service.objects.filter(co_shipping = True).exclude(parent_package__shipped_date = None).count()
			shipped_pack_num =   Service.objects.filter(co_shipping = False).exclude(parent_package__shipped_date = None).count()

			return render(request, self.template_name,{
			"not_ready_co_pack_num":not_ready_co_pack_num,
			"not_ready_pack_num":not_ready_pack_num,
			"ready_co_pack_num":ready_co_pack_num,
			"ready_pack_num":ready_pack_num,
			"shipped_co_pack_num":shipped_co_pack_num,
			"shipped_pack_num":shipped_pack_num,
			})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

	def post(self, request):
		form = TrackingForm(request.POST)
		if form.is_valid():
			tracking_num = form.cleaned_data['cust_tracking_num']
			packages = Service.objects.filter(cust_tracking_num = tracking_num)
			if packages.count() == 0:
				packages = Service.objects.filter(id = tracking_num)
				if packages.count() == 0:
					messages.error(request, _("Package '"+tracking_num + "' was not found!"))
			return render(request, self.template_name, {'packages': packages})
		else:
			return redirect(reverse('wh_home'))

class EnterWeightCoPackage(TemplateView):
	template_name = 'warehouse/enter_weight_copackage.html'

	def get(self, request, service_id):
		if request.user.is_staff or request.user.is_superuser:
			package = Service.objects.get(id=service_id)
			vol_form = EnterVolumeForm()
			form = CoPriceCalForm(instance=package)
			return render(request, self.template_name,
						{'form': form,
						'vol_form':vol_form,
						'package':package,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

	def post(self, request, service_id):
		package = Service.objects.get(id=service_id)

		vol_form = EnterVolumeForm(request.POST)
		form = CoPriceCalForm(request.POST, instance=package)
		if vol_form.is_valid() and form.is_valid():
			l = vol_form.cleaned_data['length']
			w = vol_form.cleaned_data['width']
			h = vol_form.cleaned_data['height']

			pack = form.save(commit = False)
			pack.volume_weight = math.ceil(l*w*h/500)/10

			pack.ship_carrier = ''
			pack.issue = ''

			if pack.wh_received and pack.ship_to_col:
				if pack.wh_received.country.lower() == 'china':
					fc = 'cn'
				elif pack.wh_received.country.lower() == 'united states' or pack.wh_received.country.lower() == 'usa' or pack.wh_received.country.lower() == 'us':
					fc = 'us'
				else:
					fc = pack.wh_received.country.lower()

				if pack.ship_to_col.country.lower() == 'china':
					tc = 'cn'
				elif pack.ship_to_col.country.lower() == 'united states' or pack.ship_to_col.country.lower() == 'usa' or pack.ship_to_col.country.lower() == 'us':
					tc = 'us'
				else:
					tc = pack.ship_to_col.country.lower()
				try:
					price = PriceRate.objects.get(
							category='ship',
							from_country=fc,
							to_country = tc,
							package_type = pack.package_type,
							carrier = '',
							)
				except:
					price = None
			else:
				price = None

			if price:
				if pack.weight > pack.volume_weight:
					pack.shipping_fee = float ( price.avg_weight_price) * float ( pack.weight) * 10
				else:
					pack.shipping_fee = float ( price.avg_weight_price) * float ( pack.volume_weight) * 10

				pack.currency = price.shipping_currency

			if not pack.wh_received_date:
				pack.wh_received_date = date.today()
			pack.ready_date = date.today()
			pack.emp_pack = request.user.employee
			pack.save()

			send_copackage_ready_to_pay_email(pack.id)
			return redirect(reverse('copackage_weight',args = (pack.id,)))
		else:
			return render(request, self.template_name, {'form': form})



class EnterWeightParentPackage(TemplateView):
	template_name = 'warehouse/enter_weight_parent_package.html'

	def get(self, request, parent_id):
		if request.user.is_staff or request.user.is_superuser:
			parent_package = ParentPackage.objects.get(id=parent_id)
			vol_form = EnterVolumeForm()
			form = PriceCalForm(instance=parent_package)
			return render(request, self.template_name,
						{'form': form,
						'vol_form':vol_form,
						'parent_package':parent_package,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

	def post(self, request, parent_id):
		parent_package = ParentPackage.objects.get(id=parent_id)
		vol_form = EnterVolumeForm(request.POST)
		form = PriceCalForm(request.POST, instance=parent_package)

		if vol_form.is_valid() and form.is_valid():

			l = vol_form.cleaned_data['length']
			w = vol_form.cleaned_data['width']
			h = vol_form.cleaned_data['height']

			pack = form.save(commit = False)
			pack.volume_weight = math.ceil(l*w*h/500)/10
			sub = pack.service_set.first()

			if sub.wh_received and sub.ship_to_add:

				if sub.wh_received.country.lower() == 'china':
					fc = 'cn'
				elif sub.wh_received.country.lower() == 'united states' or sub.wh_received.country.lower() == 'usa' or sub.wh_received.country.lower() == 'us':
					fc = 'us'
				else:
					fc = sub.wh_received.country.lower()

				if sub.ship_to_add.country.lower() == 'china':
					tc = 'cn'
				elif sub.ship_to_add.country.lower() == 'united states' or sub.ship_to_add.country.lower() == 'usa' or sub.ship_to_add.country.lower() == 'us':
					tc = 'us'
				else:
					tc = sub.ship_to_add.country.lower()

				if pack.carrier =='EMS' :
					if pack.weight >= 20.5:
						pack.carrier = "%s+"%(pack.carrier)
				else:
					if pack.volume_weight >= 20.5 or pack.weight >= 20.5:
						pack.carrier = "%s+"%(pack.carrier)

				try:
					price = PriceRate.objects.get(
							category='ship',
							from_country=fc,
							to_country = tc,
							package_type = pack.package_type,
							carrier = pack.carrier,
							)
				except:
					price = None

			else:
				price = None

			if price:
				if pack.carrier =='EMS' or pack.carrier =='EMS+':

					shipping_amount = float ( price.first_weight_price) + float ( price.next_weight_price) * math.ceil((float(pack.weight)-0.5)*2)
				else:
					if pack.weight > pack.volume_weight:
						shipping_amount = float ( price.first_weight_price) + float ( price.next_weight_price) *  math.ceil((float(pack.weight)-0.5)*2)
					else:
						shipping_amount = float ( price.first_weight_price) + float ( price.next_weight_price) *  math.ceil((float(pack.volume_weight)-0.5)*2)
				pack.package_amount = shipping_amount*1.1 + pack.get_total()
				pack.currency = price.shipping_currency
			else:
				messages.error(request, _("Cannot find the match price!"))
			pack.packed_date = date.today()
			if request.user.employee:
				pack.emp_pack = request.user.employee
			pack.save()
			send_package_ready_to_pay_email(pack.id)
			return redirect(reverse('parent_package_weight',args = (pack.id,)))
		else:
			return render(request, self.template_name, {'form': form})

class ShipParentPackage(TemplateView):
	template_name = 'warehouse/ship_parent_package.html'

	def get(self, request, parent_id):
		if request.user.is_staff or request.user.is_superuser:
			parent_package = ParentPackage.objects.get(id=parent_id)
			return render(request, self.template_name,
						{'parent_package':parent_package,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

	def post(self, request, parent_id):
		if request.user.is_staff or request.user.is_superuser:
			parent_package = ParentPackage.objects.get(id=parent_id)
			form = TrackingForm(request.POST)
			if form.is_valid():
				parent_package.tracking_num = form.cleaned_data['cust_tracking_num']
				parent_package.shipped_date = date.today()
				parent_package.save()
			return redirect(reverse('ship_parent_package',args = (parent_package.id,)))
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))




class EnterIssue(TemplateView):
	template_name = 'warehouse/enter_issue.html'

	def get(self, request, service_id):
		if request.user.is_staff or request.user.is_superuser:
			package = Service.objects.get(id=service_id)
			return render(request, self.template_name, {'package': package,})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))


	def post(self, request, service_id):
		package = Service.objects.get(id=service_id)
		form = IssueForm(request.POST)
		if form.is_valid():
			package.issue = form.cleaned_data['issue']
			if not package.wh_received_date:
				package.wh_received_date = date.today()
			package.save()
		return redirect(reverse('not_ready_copackages'))


def packageReceived(request, service_id):
	if request.POST:
		package = Service.objects.get(id=service_id)
		if not package.wh_received_date:
			package.wh_received_date = date.today()
			package.save()
		return HttpResponse()
