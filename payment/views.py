# HTML Variables for PayPal Payments Standard
# https://developer.paypal.com/webapps/developer/docs/classic/paypal-payments-standard/integration-guide/Appx_websitestandard_htmlvariables/

from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

from main.models import OrderSet, Service
from django.views.decorators.csrf import csrf_exempt

def payment_process(request):
	order_set_id = request.session.get('order_set_id')
	discount_amount = request.session.get('discount_amount')
	orderSet = get_object_or_404(OrderSet, id = order_set_id)
	host = request.get_host()


	if orderSet.coupon:
		paypal_dict = {
			"business" : settings.PAYPAL_RECEIVER_EMAIL,
			"amount": (orderSet.total_amount + orderSet.insurance),
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
			"amount": (orderSet.total_amount + orderSet.insurance),
			"currency_code": orderSet.currency,
			"item_name": "{} package(s)/order(s) ({})".format((orderSet.service_set.all().count()+orderSet.parentpackage_set.all().count()), orderSet.get_insurance_display()),
			"invoice": orderSet.id,
			"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
			"return": 'http://{}{}'.format(host, reverse('pdt_return_url')),
			"cancel_return": 'http://{}{}'.format(host, reverse('packagecart')),
		}
	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	return render(request, 'payment/process.html', {'orderSet': orderSet,
													'form' : form,
													'discount_amount':discount_amount})

from django.views.decorators.http import require_GET
from paypal.utils import warn_untested


def process_pdt(request):
	"""
	Payment data transfer implementation:
	https://developer.paypal.com/webapps/developer/docs/classic/products/payment-data-transfer/

	This function returns a tuple of (pdt_obj, failed)
	pdt_obj is an object of type PayPalPDT
	failed is a flag that is True if the input data didn't pass basic validation.

	Note: even for failed=False You must still check the pdt_obj is not flagged i.e.
	pdt_obj.flag == False
	"""

	pdt_obj = None
	txn_id = request.GET.get('tx')
	failed = False
	if txn_id is not None:
		# If an existing transaction with the id tx exists: use it
		try:
			pdt_obj = PayPalPDT.objects.get(txn_id=txn_id)
			print('----------------------pdt_obj------------1-------------')
		except PayPalPDT.DoesNotExist:
			# This is a new transaction so we continue processing PDT request
			pass

		if pdt_obj is None:
			print('----------------------pdt_obj---------2----------------')
			form = PayPalPDTForm(request.GET)
			if form.is_valid():
				print('----------------------pdt_obj-------------3------------')
				try:
					pdt_obj = form.save(commit=False)
					print('----------------------pdt_obj-------------4------------')
				except Exception as e:
					warn_untested()
					error = repr(e)
					failed = True
			else:
				print('----------------------pdt_obj-------------5------------')
				warn_untested()
				error = form.errors
				failed = True

			if failed:
				print('----------------------pdt_obj-----------------6--------')
				warn_untested()
				pdt_obj = PayPalPDT()
				pdt_obj.set_flag("Invalid form. %s" % error)

			pdt_obj.initialize(request)

			if not failed:
				print('----------------------pdt_obj-------------7------------')
				# The PDT object gets saved during verify
				pdt_obj.verify()
			print('----------------------pdt_obj--------------------8-----')
			print(pdt_obj)
	else:
		pass  # we ignore any PDT requests that don't have a transaction id

	return (pdt_obj, failed)

@require_GET
def payment_processed(request):
	pdt_obj, failed = process_pdt(request)
	context = {"failed": failed, "pdt_obj": pdt_obj}
	if not failed:

		# WARNING!
		# Check that the receiver email is the same we previously
		# set on the business field request. (The user could tamper
		# with those fields on payment form before send it to PayPal)

		if pdt_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:

			print('yes')
			return render(request, reverse('packages'), context)
	return render(request, reverse('packagecart'), context)
