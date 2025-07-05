from allauth.account.models import get_emailconfirmation_model
from django.views.generic import TemplateView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


class ConfirmEmailTemplateView(TemplateView):
    template_name = "users/auth/email/confirm_email.html"

class PasswordResetTemplateView(TemplateView):
    template_name = "users/auth/password_reset/password_reset.html"

class PasswordResetConfirmView(TemplateView):
    template_name = "users/auth/password_reset/password_reset_confirm.html"

class CustomConfirmEmailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        key = self.kwargs["key"]

        model = get_emailconfirmation_model()
        emailconfirmation = model.from_key(key)

        if not emailconfirmation:
            raise NotFound("Ссылка невалидна или истек срок действия")

        if emailconfirmation.email_address.verified:
            raise ValidationError("Почта уже подтверждена!")

        emailconfirmation.email_address.verified = True
        emailconfirmation.email_address.save()

        # Return JSON response for API
        return Response({
            'message': f'Почта {emailconfirmation.email_address} удачно подтверждена!',
            'redirect_url': '/login/'
        })