from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
# , permission_required



urlpatterns = [
    path('', views.HomeView.as_view(), name='wh_home'),
    path('coshipping-packages/not-ready', login_required(views.NotReadyCoPackages.as_view()), name='not_ready_copackages'),
    path('direct-shipping-packages/not-ready', login_required(views.NotReadyDirectPackages.as_view()), name='not_ready_direct_packages'),
    path('<int:service_id>/co-shipping/weight', views.EnterWeightCoPackage.as_view(), name='copackage_weight'),
    path('<int:parent_id>/weight', views.EnterWeightParentPackage.as_view(), name='parent_package_weight'),
    path('<int:parent_id>/detail', views.ParentPackageDetail.as_view(), name='parent_package_detail'),
    path('<int:service_id>/issue', views.EnterIssue.as_view(), name='issue'),
    path('<int:service_id>/received', views.packageReceived, name='received'),
]
