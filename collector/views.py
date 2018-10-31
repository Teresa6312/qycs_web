from .models import Review, Question, ReviewResponse, QuestionResponse
from main.models import CollectionPoint, Resource
from main.forms import  NewUserChangeForm

from .forms import MessageForm, ResponseForm, ColChangeForm, ColCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _



class ColRegisterView(TemplateView):
	template_name = 'collector/colregister.html'

	def get(self, request):
		try:
			return redirect(reverse('collection_point_view',args = (request.user.collectionpoint.pk,)))
		except:
			userform = NewUserChangeForm(instance=request.user)
			userform.fields['password'].required = False
			userform.fields['phone'].required = True
			userform.fields['first_name'].required = True
			userform.fields['last_name'].required = True
			colform = ColCreationForm()
			try:
				text = Resource.objects.get(title='collection_point_term')
				term = text.english_content
			except:
				term = _('Term is not available Right now.')
			return render(request, self.template_name, {'colform': colform,
														'userform': userform,
														"term": term,
														})


	def post(self, request):
		userform  = NewUserChangeForm(request.POST, instance=request.user)
		userform.fields['password'].required = False
		colform = ColCreationForm(request.POST, request.FILES)
		if colform.is_valid() and userform.is_valid():
			collector = colform.save(commit=False)
			collector.collector = request.user
			collector.save()
			user = userform.save(commit=False)
			user.default_col = collector
			user.save()
			messages.info(request, _('Thank you for applied collection point. We will process your application in a week.'))
			return redirect(reverse('account'))
		else:
			return render(request, self.template_name, {
					 'colform': colform,
					 'userform': userform,
					 })

class CollectorUpdateView(TemplateView):
	template_name = 'collector/collector_update.html'

	def get(self, request):
		if request.user.collectionpoint:
			form = ColChangeForm(instance = request.user.collectionpoint)
			return render(request, self.template_name, {'form': form})
		else:
			return redirect(reverse('colregister'))

	def post(self, request):
		try:
			col = CollectionPoint.objects.get(collector = request.user)
			form = ColChangeForm(request.POST, request.FILES, instance=col)
			if form.is_valid():
				update = form.save(commit=False)
				if 'absent_start' in form.changed_data or 'absent_end' in form.changed_data:
					if update.absent_start:
						if update.absent_start< date.today() or not update.absent_end or update.absent_start>update.absent_end:
							if not update.absent_end:
								errors = form._errors.setdefault("absent_end", ErrorList())
								errors.append(_("This field is required after you entered the Unavailable Start Date."))
							if update.absent_start>update.absent_end:
								errors = form._errors.setdefault("absent_end", ErrorList())
								errors.append(_("Enter a valid date."))
							if update.absent_start< date.today():
								errors = form._errors.setdefault("absent_start", ErrorList())
								errors.append(_("Enter a valid date."))
							return render(request, self.template_name, {'form': form,})
					elif update.absent_end:
						if not update.absent_start:
							errors = form._errors.setdefault("absent_start", ErrorList())
							errors.append(_("This field is required after you entered the Unavailable End Date."))
							return render(request, self.template_name, {'form': form,})

				update.save()
				return redirect(update.get_absolute_url())
			else:
				return render(request, self.template_name, {'form': form,
															})
		except:
			return render(request, self.template_name)

class CollectionPointDetailView(TemplateView):
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
		if "type" in request.POST:
			response = ResponseForm(request.POST)
			if response.is_valid():
				if request.POST.get('type')=='review':

					new = ReviewResponse(creater=request.user,
					responseto=Review.objects.get(pk=response.cleaned_data['response_for']),
					meaasage=response.cleaned_data['response']
					)
					new.save()
				elif request.POST.get('type')=='question':

					new = QuestionResponse(creater=request.user,
					responseto=Question.objects.get(pk=response.cleaned_data['response_for']),
					meaasage=response.cleaned_data['response']
					)
					new.save()
			else:

				return render(request, self.template_name, {'collector': collector})
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
					messages.error(request,"Input Failure")
					return render(request, self.template_name, {'collector': collector})
			else:
				messages.error(request,"Input Failure")
				return render(request, self.template_name, {'collector': collector})

		return redirect(reverse('collection_point_view',args = (col_pk,)))
