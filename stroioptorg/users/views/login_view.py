from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.generic import FormView

from users.utils import AnonymousRequiredMixin


class LoginView(AnonymousRequiredMixin, FormView):
    template_name = 'users/auth/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('main:home')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['google_client_id'] = settings.GOOGLE_OAUTH_CLIENT_ID
        context_data['google_callback_uri'] = settings.GOOGLE_OAUTH_CALLBACK_URL
        return context_data