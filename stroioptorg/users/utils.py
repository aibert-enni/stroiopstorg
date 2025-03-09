from django.shortcuts import redirect
from django.views import View

class AnonymousRequiredMixin:
    """Mixin для проверки, что пользователь не аутентифицирован."""
    redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
