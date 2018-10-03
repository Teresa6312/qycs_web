from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    url(r'^process/$', views.payment_process, name='process'),
]
