from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from main.models import OrderSet
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from paypal.standard.pdt.views import process_pdt
from django.contrib import messages

@require_GET
def return_view(request):
    print('----------------------------request-------------------------------')
    print(request)
    pdt_obj, failed = process_pdt(request)
    context = {"failed": failed, "pdt_obj": pdt_obj}
    print(context)
    # if not failed:
    #
    #     # WARNING!
    #     # Check that the receiver email is the same we previously
    #     # set on the business field request. (The user could tamper
    #     # with those fields on payment form before send it to PayPal)
    #
    #     if pdt_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:
    #
    #         # ALSO: for the same reason, you need to check the amount
    #         # received etc. are all what you expect.
    #
    #         # Do whatever action is needed, then:
    #         messages.info(request, _('paid'))
    #         return redirect(reverse('userpackage'))
    #     messages.info(request, _('fail'))
    #     return redirect(reverse('package_cart'))
    messages.info(request, failed)
    return redirect(reverse('packagecart'))


def payment_process(request):
    order_set_id = request.session.get('order_set_id')
    orderSet = get_object_or_404(OrderSet, id = order_set_id)
    host = request.get_host()
    # What you want the button to do.
    if orderSet.coupon:
        paypal_dict = {
            "business" : settings.PAYPAL_RECEIVER_EMAIL,
            "amount": (orderSet.total_amount + orderSet.insurance),
            "currency_code": orderSet.currency,
            "item_name": "{} packages".format(orderSet.service_set.all().count()),
            "discount_rate": orderSet.coupon.discount,
            "invoice": orderSet.id,
            "notify_url": 'http://{}{}'.format(host, reverse('payment:process')),
            "return": 'http://{}{}'.format(host, reverse('payment:pdt_return_url')),
            "cancel_return": 'http://{}{}'.format(host, reverse('packagecart')),
        }
    else:
        paypal_dict = {
            "business" : settings.PAYPAL_RECEIVER_EMAIL,
            "amount": orderSet.total_amount,
            "currency_code": orderSet.currency,
            "item_name": "{} package(s)/order(s)".format(orderSet.service_set.all().count()),
            "invoice": orderSet.id,
            "notify_url": 'http://{}{}'.format(host, reverse('payment:process')),
            "return": 'http://{}{}'.format(host, reverse('payment:pdt_return_url')),
            "cancel_return": 'http://{}{}'.format(host, reverse('packagecart')),
        }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'orderSet': orderSet,
                                                    'form' : form})
