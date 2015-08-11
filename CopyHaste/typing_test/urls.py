from django.conf.urls import url
from .views import play_view, multi_play_view

urlpatterns = [
    url(r'^$', play_view, name='typing_test'),
    url(r'^multi/', multi_play_view, name='multi_typing_test'),
]
