from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterForm
from users.models import User
from users.utils import AnonymousRequiredMixin


class RegisterView(AnonymousRequiredMixin, CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/auth/register.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)