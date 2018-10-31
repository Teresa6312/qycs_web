from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from collector import views as col_views
from main import views as main_views

from django.contrib.sitemaps.views import sitemap
from main.sitemap import CollectionPointSitemap, ResourceSitemap, StaticViewSitemap

sitemaps = {
    'collectionpoints': CollectionPointSitemap,
    'information': ResourceSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', include('main.urls')),

    path('collector/', include('collector.urls')),
    path('payment/', include(('payment.urls', 'reviews'), namespace='payment')),
    path('guanjia/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('collection-point/<int:col_pk>/view', col_views.CollectionPointDetailView.as_view(), name='collection_point_view'),
    path('information/<str:title>/', main_views.InformationView.as_view(), name='information'),
    path('_/', include('django.conf.urls.i18n')),
    path('gloabl-shop/', main_views.ShoppingView.as_view(), name='shopping'),
    path('collection-points/', main_views.CollectionPointView.as_view(), name='collection_points'),

    path('auth/', include('social_django.urls', namespace='social')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
