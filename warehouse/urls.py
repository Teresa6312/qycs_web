from . import views, list_views
from django.urls import path
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    path('', views.HomeView.as_view(), name='wh_home'),
    path('coshipping-packages/not-ready', login_required(list_views.NotReadyCoPackages.as_view()), name='not_ready_copackages'),
    path('direct-shipping-packages/not-ready', login_required(list_views.NotReadyDirectPackages.as_view()), name='not_ready_direct_packages'),
    path('coshipping-packages/ready', login_required(list_views.ReadyCoPackages.as_view()), name='ready_copackages'),
    path('direct-shipping-packages/ready', login_required(list_views.ReadyDirectPackages.as_view()), name='ready_direct_packages'),
    path('coshipping-packages/shipped', login_required(list_views.ShippedCoPackages.as_view()), name='shipped_copackages'),
    path('direct-shipping-packages/shipped', login_required(list_views.ShippedDirectPackages.as_view()), name='shipped_direct_packages'),
    path('<int:service_id>/co-shipping/weight', login_required(views.EnterWeightCoPackage.as_view()), name='copackage_weight'),
    path('<int:parent_id>/weight', login_required(views.EnterWeightParentPackage.as_view()), name='parent_package_weight'),
    path('<int:parent_id>/detail',login_required( views.ParentPackageDetail.as_view()), name='parent_package_detail'),
    path('<int:service_id>/issue', login_required(views.EnterIssue.as_view()), name='issue'),
    path('<int:service_id>/received', login_required(views.packageReceived), name='received'),
]
