from django.views.generic import FormView
from .models import CNHProfile
from .forms import ProfileSettingsForm


class ProfileFormView(FormView):
    template_name = 'edit_profile.html'
    form_class = ProfileSettingsForm
    success_url = '/profile/'

    def get_form(self, form_class=ProfileSettingsForm):
        try:
            profile = CNHProfile.objects.get(user=self.request.user)
            return ProfileSettingsForm(
                instance=profile, **self.get_form_kwargs())
        except (TypeError, CNHProfile.DoesNotExist):
            return ProfileSettingsForm(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(ProfileFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        profile = form.save(commit=False, request=self.request)
        profile.user = self.request.user
        profile.save()
        return super(ProfileFormView, self).form_valid(profile)
