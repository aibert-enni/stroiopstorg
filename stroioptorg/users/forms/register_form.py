from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Region


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    full_name = forms.CharField(required=True)
    region = forms.ModelChoiceField(required=True, queryset=Region.objects.all(), widget=forms.Select())

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'region', 'password1', 'password2',)