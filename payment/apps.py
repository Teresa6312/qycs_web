from django.apps import AppConfig
from django.db.models.signals import pre_save


class PaymentConfig(AppConfig):
    name = 'payment'

    # def ready(self):
    #     # importing model classes
    #     from paypal.standard.ipn.models import PayPalIPN
    #     from .hooks import payment_paid
    #
    #     pre_save.connect(payment_paid, sender=PayPalIPN)
