from django.views.generic import CreateView, TemplateView
from .models import Matches, UserScores
from django.contrib.auth.models import User


class UserScoreView(TemplateView):
    template_name = 'scores.html'

    def get_context_data(self, **kwargs):
        context = super(UserScoreView, self).get_context_data(**kwargs)
        try:
            context['scores'] = UserScores.objects.all()
        except UserScores.DoesNotExist:
            pass
        return context


class MatchFormView(CreateView):
    model = Matches
    fields = ['winner', 'loser']
    success_url = '/scores'


class ScoreFormView(CreateView):
    model = UserScores
    fields = ['wpm_gross', 'wpm_net', 'mistakes']
    success_url = '/scores'

    def form_valid(self, form):
        score = form.save(commit=False)
        score.user = self.request.user
        score.save()
        return super(ScoreFormView, self).form_valid(form)
