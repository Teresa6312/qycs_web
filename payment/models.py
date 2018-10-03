# from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
# from paypal.standard.models import ST_PP_COMPLETED
# from django.conf import settings
# from main.models import OrderSet, Service
# from paypal.standard.ipn.models import PayPalIPN
#
# # https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
# def payment_paid(sender, **kwargs):
#     ipn_obj = sender
#     print('---------------------------------payment-------------------------------------')
#     print(ipn_obj)
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         order = OrderSet.objects.get(id = ipn_obj.invoice)
#         if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
#             return
#
#         if ipn_obj.mc_gross == order.total_amount and ipn_obj.mc_currency == order.currency:
#             if order.coupon:
#                 for pack in order.package_set.all:
#                     package = Service.objects.get(id = pack.id)
#                     package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
#             else:
#                 for pack in order.package_set.all:
#                     package = Service.objects.get(id = pack.id)
#                     package.paid_amount = package.get_total()
#         else:
#             return
#     else:
#         return
#
# valid_ipn_received.connect(payment_paid)
#
# def payment_fail(sender, **kwargs):
#     ipn_obj = sender
#     print('---------------------------------payment-------------------------------------')
#     print(ipn_obj)
# invalid_ipn_received.connect(payment_fail)
