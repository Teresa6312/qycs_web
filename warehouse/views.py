from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from main.models import Service, PriceRate
from django.http import HttpResponseRedirect
from .forms import PriceCalForm, EnterVolumeForm, IssueForm
from django.urls import reverse
import math
from datetime import date

class NotReadyCoPackages(TemplateView):
	template_name = 'warehouse/not_ready_copackages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(shipping_fee=None, co_shipping = True).order_by('cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("You have no right to access the page."))
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class EnterWeight(TemplateView):
	template_name = 'warehouse/enter_weight.html'


	def get(self, request, service_id):
		vol_form = EnterVolumeForm()
		form = PriceCalForm()
		package = Service.objects.get(id=service_id)
		return render(request, self.template_name,
					{'form': form,
					'vol_form':vol_form,
					'package':package,
					})

	def post(self, request, service_id):
		package = Service.objects.get(id=service_id)
		vol_form = EnterVolumeForm(request.POST)
		form = PriceCalForm(request.POST, instance=package)
		if vol_form.is_valid() and form.is_valid():
			l = vol_form.cleaned_data['length']
			w = vol_form.cleaned_data['width']
			h = vol_form.cleaned_data['height']

			pack = form.save(commit = False)

			pack.volume_weight = math.ceil(l*w*h/500)/10

			pack.ship_carrier = ''
			pack.issue = ''

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

			price = PriceRate.objects.get(
					category='ship',
					from_country=fc,
					to_country = tc,
					package_type = pack.package_type,
					carrier = '',
					)
			if price:
				if pack.weight > pack.volume_weight:
					pack.shipping_fee = float ( price.avg_weight_price) * float ( pack.weight) * 10
				else:
					pack.shipping_fee = float ( price.avg_weight_price) * float ( pack.volume_weight) * 10

				pack.currency = price.shipping_currency

			if not pack.wh_received_date:
				pack.wh_received_date = date.today()
			pack.ready_date = date.today()

			pack.save()

			return redirect(reverse('not_ready_copackages'))
		else:
			return render(request, self.template_name, {'form': form})

class EnterIssue(TemplateView):
	template_name = 'warehouse/enter_issue.html'

	def get(self, request, service_id):
		package = Service.objects.get(id=service_id)
		return render(request, self.template_name, {'package': package,})

	def post(self, request, service_id):
		package = Service.objects.get(id=service_id)
		form = IssueForm(request.POST)
		if form.is_valid():
			package.issue = form.cleaned_data['issue']
			package.save()
		return redirect(reverse('not_ready_copackages'))
