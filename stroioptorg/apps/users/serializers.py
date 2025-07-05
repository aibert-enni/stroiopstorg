from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utils.validators import firstname_validator, lastname_validator, phone_number_validator


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')

        return super().validate(attrs)

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    firstname = serializers.CharField(required=True, validators=[firstname_validator])
    lastname = serializers.CharField(required=True, validators=[lastname_validator])
    phone_number = serializers.CharField(required=True, validators=[phone_number_validator])


    def validate(self, attrs):
        attrs['username'] = attrs.get('email')

        return super().validate(attrs)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['firstname'] = self.validated_data.get('firstname', '')
        data['lastname'] = self.validated_data.get('lastname', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.firstname = self.cleaned_data.get('firstname')
        user.lastname = self.cleaned_data.get('lastname')
        user.phone_number = self.cleaned_data.get('phone_number')

        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
