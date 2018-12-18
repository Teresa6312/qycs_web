from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from main.models import Service
from django.http import HttpResponseRedirect
from .forms import PriceCalForm, EnterVolumeForm
from django.urls import reverse

class NotReadyCoPackages(TemplateView):
	template_name = 'warehouse/not_ready_copackages.html'

	def get(self, request):
		if request.user.is_staff or request.user.is_superuser:
			packages = Service.objects.filter(paid_amount=None, co_shipping = True).order_by('cust_tracking_num')

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
		form = EnterWeightForm(request.POST)
		if form.is_valid():
			l = form.cleaned_data['length']
			w = form.cleaned_data['width']
			h = form.cleaned_data['height']
			weight = form.cleaned_data['weight']
			volume_weight = l*w*h/5000
			if weight < volume_weight:
				weight = volume_weight


			return redirect(reverse('not_ready_packages'))
		else:
			return render(request, self.template_name, {'form': form})

class EnterIssue(TemplateView):
	template_name = 'warehouse/enter_issue.html'

	def get(self, request, service_id):
		return render(request, self.template_name)
