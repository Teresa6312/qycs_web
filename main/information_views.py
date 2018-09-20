from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

class CustomerServiceView(TemplateView):
	template_name = 'main/customer_service.html'

	def get(self, request):
		return render(request, self.template_name)

class AboutUsView(TemplateView):
	template_name = 'main/about_us.html'

	def get(self, request):
		return render(request, self.template_name)

class FQAView(TemplateView):
	template_name = 'main/fqa.html'

	def get(self, request):
		return render(request, self.template_name)

class FQAView(TemplateView):
	template_name = 'main/fqa.html'

	def get(self, request):
		return render(request, self.template_name)
