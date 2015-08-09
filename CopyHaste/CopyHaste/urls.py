from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import home_view

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_view, name='homepage'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('cnh_profile.urls')),
)
