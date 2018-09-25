from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

# , permission_required



urlpatterns = [
    path('register/',  login_required(views.ColRegisterView.as_view()), name = 'colregister'),
    path('profile/update', login_required(views.CollectorUpdateView.as_view()), name='collector_update'),
]
