# Generated by Django 5.1.4 on 2025-04-02 06:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='firstname',
            field=models.CharField(max_length=120, validators=[django.core.validators.RegexValidator(message='Имя может содержать только буквы', regex='^[A-Za-zА-Яа-яЁё\\-]+$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastname',
            field=models.CharField(max_length=120, validators=[django.core.validators.RegexValidator(message='Фамилия может содержать только буквы', regex='^[A-Za-zА-Яа-яЁё\\-]+$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='mail',
            field=models.CharField(max_length=120, validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
