from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.conf import settings
from main.models import OrderSet, Service
from paypal.standard.ipn.models import PayPalIPN

# https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
def payment_paid(sender, **kwargs):
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		order = OrderSet.objects.get(id = ipn_obj.invoice)
		if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
			return

		if ipn_obj.mc_gross == order.total_amount and ipn_obj.mc_currency == order.currency:
			if order.service_set.all().count()>0:
				if order.coupon:
					for pack in order.service_set.all():
						package = Service.objects.get(id = pack.id)
						package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
						package.save()
				else:
					for pack in order.service_set.all():
						package = Service.objects.get(id = pack.id)
						package.paid_amount = package.get_total()
						package.save()

# parent_package
			count = order.parentpackage_set.all().count()
			if count > 0:
				if order.coupon:
					for parent_pack in order.parentpackage_set.all():
						parent_pack.paid_amount = parent_pack.package_amount*(1-order.coupon.discount/100)
						for pack in parent_pack.service_set.all():
							package = Service.objects.get(id = pack.id)
							package.paid_amount = parent_pack.package_amount*(1-order.coupon.discount/100)/count
							package.save()
				else:
					for parent_pack in order.parentpackage_set.all():
						parent_pack.paid_amount = parent_pack.package_amount
						for pack in parent_pack.service_set.all():
							package = Service.objects.get(id = pack.id)
							package.paid_amount = parent_pack.package_amount/count
							package.save()

		else:
			return
	else:
		return

valid_ipn_received.connect(payment_paid)
