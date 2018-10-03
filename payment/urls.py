from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    url(r'^process/$', views.payment_process, name='process'),
    url(r'^your_return_url/', views.return_view, name="pdt_return_url"),
]
