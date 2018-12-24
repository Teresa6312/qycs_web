# HTML Variables for PayPal Payments Standard
# https://developer.paypal.com/webapps/developer/docs/classic/paypal-payments-standard/integration-guide/Appx_websitestandard_htmlvariables/

from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

from main.models import OrderSet, Service
from django.views.decorators.csrf import csrf_exempt

def payment_process(request):
	if request.GET:
		try:
			order_set_id = request.session.get('order_set_id')
			discount_amount = request.session.get('discount_amount')
			del request.session['order_set_id']
			del request.session['discount_amount']
		except:
			return redirect(reverse('packagecart'))

		orderSet = get_object_or_404(OrderSet, id = order_set_id)

		host = request.get_host()

		total = orderSet.total_amount + orderSet.insurance
		if orderSet.coupon:
			paypal_dict = {
				"business" : settings.PAYPAL_RECEIVER_EMAIL,
				"amount": total,
				"currency_code": orderSet.currency,
				"item_name": "{} package(s)/order(s) ({})".format((orderSet.service_set.all().count()+orderSet.parentpackage_set.all().count()), orderSet.get_insurance_display()),
				"discount_amount": discount_amount,
				"invoice": orderSet.id,
				"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
				"return": 'http://{}{}'.format(host, reverse('userpackage')),
				"cancel_return": 'http://{}{}'.format(host, reverse('packagecart')),
			}
		else:
			paypal_dict = {
				"business" : settings.PAYPAL_RECEIVER_EMAIL,
				"amount": total,
				"currency_code": orderSet.currency,
				"item_name": "{} package(s)/order(s) ({})".format((orderSet.service_set.all().count()+orderSet.parentpackage_set.all().count()), orderSet.get_insurance_display()),
				"invoice": orderSet.id,
				"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
				"return": 'http://{}{}'.format(host, reverse('userpackage')),
				"cancel_return": 'http://{}{}'.format(host, reverse('packagecart')),
			}
		# Create the instance.
		form = PayPalPaymentsForm(initial=paypal_dict)
		return render(request, 'payment/process.html', {'orderSet': orderSet,
														'form' : form,
														'discount_amount':discount_amount,
														'total':total})
	else:
		print(request.POST)
