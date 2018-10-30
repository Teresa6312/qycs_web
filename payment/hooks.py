from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.conf import settings
from main.models import OrderSet, Service
from paypal.standard.ipn.models import PayPalIPN

# https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
def payment_paid(sender, **kwargs):
    ipn_obj = sender
    print('---------------------------------payment--------payment_paid-----------------------------')
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = OrderSet.objects.get(id = ipn_obj.invoice)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            print('--------------------1-------------payment--------payment_paid-----------------------------')
            return

        if ipn_obj.mc_gross == order.total_amount and ipn_obj.mc_currency == order.currency:
            print('--------------------2-------------payment--------payment_paid-----------------------------')
            if order.coupon:
                for pack in order.service_set.all:
                    package = Service.objects.get(id = pack.id)
                    package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
                    package.save()
                    print('--------------------3-------------payment--------payment_paid-----------------------------')

                    print(package.paid_amount)
            else:
                for pack in order.service_set.all:
                    package = Service.objects.get(id = pack.id)
                    package.paid_amount = package.get_total()
                    package.save()
                    print('--------------------4-------------payment--------payment_paid-----------------------------')

                    print(package.paid_amount)
        else:
            return
    else:
        return

valid_ipn_received.connect(payment_paid)

def payment_fail(sender, **kwargs):
    ipn_obj = sender
    print('---------------------------------payment----------payment_fail---------------------------')
    print(ipn_obj)
invalid_ipn_received.connect(payment_fail)
