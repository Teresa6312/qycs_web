from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from main.models import Service, PriceRate, ParentPackage
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import math
from datetime import date
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import ShipCopackageForm

class NotReadyCoPackages(TemplateView):
	template_name = 'warehouse/not_ready_copackages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(paid_amount=None, co_shipping = True).order_by('cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

class NotReadyDirectPackages(TemplateView):
	template_name = 'warehouse/not_ready_direct_packages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(parent_package__paid_amount=None, co_shipping = False).order_by('-parent_package__paid_amount','-parent_package','cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

class ReadyCoPackages(TemplateView):
	template_name = 'warehouse/ready_copackages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(co_shipping = True, parent_package__shipped_date = None).exclude(paid_amount=None).order_by('cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

	def post(self,request):
		if request.user.is_staff or request.user.is_superuser:

			form = ShipCopackageForm(request.POST)
			if form.is_valid():
				parent_package = ParentPackage.objects.create(carrier = form.cleaned_data['carrier'], tracking_num = form.cleaned_data['tracking_num'],shipped_date=date.today())
				for pack in form.cleaned_data['package_set']:
					package = Service.objects.get(id = pack.id )
					package.parent_package = parent_package
					package.save()

			return redirect(reverse('ready_copackages'))
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

class ReadyDirectPackages(TemplateView):
	template_name = 'warehouse/ready_direct_packages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(co_shipping = False, parent_package__shipped_date = None).exclude(parent_package__paid_amount=None).order_by('-parent_package','cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))


class ShippedCoPackages(TemplateView):
	template_name = 'warehouse/shipped_copackages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(co_shipping = True).exclude(parent_package__shipped_date = None).order_by('cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))

class ShippedDirectPackages(TemplateView):
	template_name = 'warehouse/shipped_direct_packages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(co_shipping = False).exclude(parent_package__shipped_date = None).order_by('-parent_package','cust_tracking_num')

			return render(request, self.template_name,
						{'packages': packages,
						})
		else:
			messages.error(request, _("Staff access only!"))
			return redirect(reverse('login'))
