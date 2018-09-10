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
    path('payment/', include('payment.urls'), namespace = 'payment'),
    path('guanjia/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('collectionpoint/<int:col_pk>/view', col_views.CollectionPointView.as_view(), name='collection_point_view'),
    path('information/<str:title>/', main_views.InformationView.as_view(), name='information'),
    path('gloabl-shop/', main_views.ShoppingView.as_view(), name='shopping'),
    path('collection-points/', main_views.CollectionPointView.as_view(), name='collection_points'),

    path('auth/', include('social_django.urls', namespace='social')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
#     # This allows the error pages to be debugged during development, just visit
#     # these url in browser to see how these error pages look like.
#     urlpatterns += [
#         # url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
#         # url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
#         # url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
#         # url(r'^500/$', default_views.server_error),
#     ]
#     if 'debug_toolbar' in settings.INSTALLED_APPS:
#         import debug_toolbar
#         urlpatterns = [
#             url(r'^__debug__/', include(debug_toolbar.urls)),
#         ] + urlpatterns
