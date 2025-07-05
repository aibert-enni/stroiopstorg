from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.users.views import RegisterView, LoginView
from users.views.email import PasswordResetTemplateView, PasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),

    # reset password
    path('password_reset/', PasswordResetTemplateView.as_view(), name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/auth/password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/auth/password_reset/password_reset_complete.html'), name='password_reset_complete'),
]
