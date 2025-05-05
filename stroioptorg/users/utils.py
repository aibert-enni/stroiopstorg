from email.message import EmailMessage

from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from rest_framework.request import Request

from users.tasks import send_email, send_emails


class AnonymousRequiredMixin:
    """Mixin для проверки, что пользователь не аутентифицирован."""
    redirect_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        ctx = {
            "user": emailconfirmation.email_address.user,
        }
        if app_settings.EMAIL_VERIFICATION_BY_CODE_ENABLED:
            ctx.update({"code": emailconfirmation.key})
        else:
            ctx.update(
                {
                    "key": emailconfirmation.key,
                    "activate_url": self.get_email_confirmation_url(
                        request, emailconfirmation
                    ),
                }
            )
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx, request)

    def send_mail(self, template_prefix: str, email: str, context: dict, request: Request = None) -> None:
        if request:
            current_site = get_current_site(request)
        else:
            current_site = None

        ctx = {
            "request": request,
            "email": email,
            "current_site": current_site,
        }
        ctx.update(context)
        msg = self.render_mail(template_prefix, email, ctx)
        if type(msg) is EmailMessage:
            send_email.delay(msg.subject, msg.body, msg.from_email, msg.to, None)
        elif type(msg) is EmailMultiAlternatives:
            send_emails.delay(msg.subject, msg.body, msg.from_email, msg.to, None)
