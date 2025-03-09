from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import  PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает пользователя с email.
        """
        if not email:
            raise ValueError('Пользователю нужно указать email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает суперпользователя с email.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Создаём пользователя с полем email вместо username
        return self.create_user(email, password, **extra_fields)

full_name_validator = RegexValidator(
    regex=r'^[А-Яа-яЁёA-Za-z\s\-]+$',
    message='ФИО может содержать только буквы, пробелы и дефисы.'
)
phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Номер телефона может содержать только цифры'
)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Почта')
    full_name = models.CharField(max_length=100, validators=[full_name_validator], verbose_name='ФИО')
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_number_validator], verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True, null=True)
    region = models.ForeignKey('users.Region', on_delete=models.SET_NULL, null=True, related_name='users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.email
