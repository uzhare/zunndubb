from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect
import urllib

from .models import Profile
from .forms import UserEmailForm, UserSettingForm

class ProfileView(DetailView):
    template_name = 'profiles/profile.html'
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'


class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/settings.html'
    model = Profile
    form_class = UserSettingForm
    success_url = "/movies"
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        return super(SettingsView, self).form_valid(form)


class DashView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/dash.html'

    def get_context_data(self, **kwargs):
        context = super(DashView, self).get_context_data(**kwargs)
        return context


class FillEmailView(FormView):
    form_class = UserEmailForm
    template_name = 'profiles/fill_email.html'

    def form_valid(self, form, *args, **kwargs):
        social_redirect_to = self.request.GET['next']
        self.request.session['saved_email'] = self.request.POST.get('email')
        return redirect('/complete/%s' % social_redirect_to)