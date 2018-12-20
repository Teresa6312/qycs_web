from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    path('', views.HomeView.as_view(), name='wh_home'),
    path('coshipping-packages/not-ready', login_required(views.NotReadyCoPackages.as_view()), name='not_ready_copackages'),
    path('direct-shipping-packages/not-ready', login_required(views.NotReadyDirectPackages.as_view()), name='not_ready_direct_packages'),
    path('<int:service_id>/weight', views.EnterWeight.as_view(), name='weight'),
    path('<int:service_id>/issue', views.EnterIssue.as_view(), name='issue'),
    path('<int:service_id>/received', views.packageReceived, name='received'),
]
