from . import views
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('<int:col_pk>/view', views.CollectionPointView.as_view(), name='collection_point_view'),

]
