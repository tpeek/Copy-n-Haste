from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import ProfileFormView


urlpatterns = [
    url(
        r'^$',
        login_required(
            TemplateView.as_view(template_name='profile.html')
        ),
        name='profile'
    ),

    url(
        r'^edit/',
        login_required(
            ProfileFormView.as_view()
        ),
        name='edit_profile'
    ),
]
