from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('processed/', views.payment_processed, name="pdt_return_url"),
]
