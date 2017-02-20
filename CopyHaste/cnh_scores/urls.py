from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import MatchScoreView, ScoreFormView, UserScoreView


urlpatterns = [
    url(
        r'^$',
        login_required(
            UserScoreView.as_view(template_name='scores.html')
        ),
        name='scores'
    ),
    url(
        r'^result$',
        login_required(
            ScoreFormView.as_view(template_name='scores.html')
        ),
        name='score_form'
    ),
    url(
        r'^match_score$',
        login_required(
            MatchScoreView.as_view(template_name='match_score.html')
        ),
        name='match_score'
    ),
]
