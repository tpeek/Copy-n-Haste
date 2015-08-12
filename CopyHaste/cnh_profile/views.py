from __future__ import division
from django.views.generic import TemplateView
from .models import CNHProfile


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        try:
            context['user'] = self.request.user
            scores = self.request.user.scores.all()
            avg_gwpm = 0
            avg_nwpm = 0
            avg_mistakes = 0
            count = 0
            for i in range(len(scores)-1):
                avg_gwpm += scores[i].wpm_gross
                avg_nwpm += scores[i].wpm_net
                avg_mistakes += scores[i].mistakes
                count += 1
            context['avg_gwpm'] = avg_gwpm/count
            context['avg_nwpm'] = avg_nwpm/count
            context['avg_mistakes'] = avg_mistakes/count
        except (ZeroDivisionError, CNHProfile.DoesNotExist):
            pass
        return context
