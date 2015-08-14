from django.conf.urls import url
from .views import play_view, matchmaking_view, multi_play_view, get_content_view, get_content_view2

urlpatterns = [
    url(r'^$', play_view, name='typing_test'),
    url(r'^multi/', multi_play_view, name='multi_typing_test'),
    url(r'^match/', matchmaking_view, name='matchmaking'),
    url(r'^content/', get_content_view),
    url(r'^content2/', get_content_view2),
]
