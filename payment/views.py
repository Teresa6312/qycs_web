from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

from main.models import OrderSet, Service
from django.views.decorators.csrf import csrf_exempt

def payment_process(request):
	order_set_id = request.session.get('order_set_id')
	orderSet = get_object_or_404(OrderSet, id = order_set_id)
	host = request.get_host()
	# What you want the button to do.
	print('--------------------------order_set_id----------------------------------------------')
	print(order_set_id)
	if orderSet.coupon:
		paypal_dict = {
			"business" : settings.PAYPAL_RECEIVER_EMAIL,
			"amount": (orderSet.total_amount + orderSet.insurance),
			"currency_code": orderSet.currency,
			"item_name": "{} packages".format(orderSet.service_set.all().count()),
			"discount_rate": orderSet.coupon.discount,
			"invoice": orderSet.id,
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return": 'http://{}{}'.format(host, reverse('userpackage')),
			"cancel_return": 'http://{}{}'.format(host, reverse('package_cart')),
		}
	else:
		paypal_dict = {
			"business" : settings.PAYPAL_RECEIVER_EMAIL,
			"amount": (orderSet.total_amount + orderSet.insurance),
			"currency_code": orderSet.currency,
			"item_name": "{} package(s)/order(s)".format(orderSet.service_set.all().count()),
			"invoice": orderSet.id,
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return": 'http://{}{}'.format(host, reverse('userpackage')),
			"cancel_return": 'http://{}{}'.format(host, reverse('packagecart')),
		}
	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'payment/process.html', {'orderSet': orderSet,
													'form' : form})

def paypal_processed(request):
	if request.POST:
		print(request)
