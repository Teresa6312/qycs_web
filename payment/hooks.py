from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.conf import settings
from main.models import OrderSet, Service, User, Coupon, ParentPackage
from paypal.standard.ipn.models import PayPalIPN

import math

from .code import paid

# https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
def payment_paid(sender, **kwargs):
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		order = OrderSet.objects.get(id = ipn_obj.invoice)
		if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
			return
		if order.tx == None or order.tx == '':
			paid(order_set_id = ipn_obj.invoice, amount = ipn_obj.mc_gross, currency = ipn_obj.mc_currency, confirmed = True)
		else:
			order.payment_confirmed = True
			order.save()
	else:
		return

valid_ipn_received.connect(payment_paid)
