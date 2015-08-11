from django.conf.urls import url
from .views import play_view

urlpatterns = [
    url(r'^', play_view, name='typing_test'),
]
