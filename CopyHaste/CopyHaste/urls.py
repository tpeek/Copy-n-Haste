from django.conf.urls import include, url
from django.contrib import admin
from .views import home_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_view, name='homepage'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('cnh_profile.urls')),
    url(r'^scores/', include('cnh_scores.urls')),
]
