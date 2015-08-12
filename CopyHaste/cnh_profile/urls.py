from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import ProfileView


urlpatterns = [
    url(
        r'^$',
        login_required(
            ProfileView.as_view()
        ),
        name='profile'
    ),
]
