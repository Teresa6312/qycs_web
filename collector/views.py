from .models import Review, Question
from main.models import CollectionPoint
from .forms import MessageForm, ResponseForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class CollectionPointView(TemplateView):
	template_name = 'collector/collection_point_view.html'

	def get(self, request, col_pk):
		try:
			collector = CollectionPoint.objects.get(pk=col_pk)
			return render(request, self.template_name, {'collector': collector})

		except ObjectDoesNotExist:
			messages.error(request,"Cannot find the Collection Point")
			return render(request, reverse('collection_points'))

	@method_decorator(login_required)
	def post(self, request, col_pk):
		collector = CollectionPoint.objects.get(pk=col_pk)
		if "response" in request.POST:
			response = ResponseForm(request.POST)

		else:
			message = MessageForm(request.POST)
			if message.is_valid():
				if "review" in request.POST:

					review = Review(creater = request.user, receiver = collector, review=message.cleaned_data['message'])
					review.save()
					messages.info(request,"Review is successfully posted!")

				elif "question" in request.POST:
					question = Question(creater = request.user, receiver = collector, question=message.cleaned_data['message'])
					question.save()
					messages.info(request,"Question is successfully created!")
				else:
					print(request.POST)

		return redirect(reverse('collection_point_view',args = (col_pk,)))
