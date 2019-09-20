from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

# , permission_required



urlpatterns = [
    path('register/',  login_required(views.ColRegisterView.as_view()), name = 'colregister'),
    path('profile/update', login_required(views.CollectorUpdateView.as_view()), name='collector_update'),
    path('parent-package/<int:pack_id>/received', login_required(views.parentPackageReceived), name='parent_pack_received'),
    path('parent-package/<int:pack_id>/detail', login_required(views.ParentPackageDetail), name='parent_pack_detail'),
    path('package/<int:service_id>/pick-up', login_required(views.pickedUp), name='pack_picked_up'),

]
