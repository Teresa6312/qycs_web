from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
# , permission_required



urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('processed/<str:tx>', views.payment_processed_done, name="paypal_return"),
]
# http://127.0.0.1:8000/payment/processed/result
