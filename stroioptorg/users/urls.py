from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users.views import RegisterView, LoginView

app_name = 'users'

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),

    # reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/auth/password_reset/password_reset.html',success_url=reverse_lazy('users:password_reset_done'),
                                                                 html_email_template_name='users/auth/password_reset/password_reset_email.html',
                                                                 email_template_name='users/auth/password_reset/password_reset_email.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/auth/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/auth/password_reset/password_reset_confirm.html',success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/auth/password_reset/password_reset_complete.html'), name='password_reset_complete'),
]
