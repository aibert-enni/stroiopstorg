# Generated by Django 5.1.4 on 2025-04-02 06:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_country_remove_user_address_remove_user_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Имя может содержать только буквы', regex='^[A-Za-zА-Яа-яЁё\\-]+$')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastname',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Фамилия может содержать только буквы', regex='^[A-Za-zА-Яа-яЁё\\-]+$')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона может содержать только цифры', regex='^\\+?1?\\d{9,15}$')], verbose_name='Номер телефона'),
        ),
    ]
