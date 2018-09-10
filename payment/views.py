from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from main.models import OrderSet


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request):
    order_set_id = request.session.get('order_set_id')
    orderSet = get_object_or_404(OrderSet, id = order_set_id)
    host = request.get_host()
    # What you want the button to do.
    paypal_dict = {
        "business" : settings.PAYPAL_RECEIVER_EMAIL,
        "amount": orderSet.total_amount,
        "currency_code": orderSet.currency,
        "item_name": "packages",
        "invoice": orderSet.id,
        "notify_url": 'http://{}{}'.format(host, reverse('your-return-view')),
        "return": 'http://{}{}'.format(host, reverse('payment:done')),
        "cancel_return": 'http://{}{}'.format(host, reverse('payment:canceled')),
        # "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        # "return": request.build_absolute_uri(reverse('your-return-view')),
        # "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'orderSet': orderSet,
                                                    'form' : form})
