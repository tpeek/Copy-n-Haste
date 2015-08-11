from django.shortcuts import render
from django.views.generic import TemplateView
from .models import UserScores
from django.contrib.auth.models import User


# Create your views here.
class UserScoreView(TemplateView):
    template_name = 'scores.html'

    def get_context_data(self, **kwargs):
        context = super(UserScoreView, self).get_context_data(**kwargs)
        try:
            context['users'] = User.objects.all()
        except UserScores.DoesNotExist:
            pass
        return context
