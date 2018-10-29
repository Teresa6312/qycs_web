from django.apps import AppConfig
from django.db.models.signals import pre_save
from .hooks import payment_paid
# from .hooks import show_me_the_money

class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        # importing model classes
        from paypal.standard.ipn.models import PayPalIPN

        # registering signals with the model's string label
        pre_save.connect(payment_paid, sender='app_label.PayPalIPN')
