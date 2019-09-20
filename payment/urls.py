from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    path('process/', views.PaymentProcessView.as_view(), name='process'),
]
