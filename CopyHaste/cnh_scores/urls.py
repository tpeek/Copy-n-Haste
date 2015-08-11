from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import UserScoreView


urlpatterns = [
    url(
        r'^$',
        login_required(
            UserScoreView.as_view(template_name='scores.html')
        ),
        name='scores'
    ),
]
