from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class UserScoreView(TemplateView):
    template_name = 'scores.html'

    def get_context_data(self, **kwargs):
        context = super(UserScoreView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['scores'] = self.request.user.scores
        return context
