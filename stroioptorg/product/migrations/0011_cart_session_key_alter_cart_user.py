# Generated by Django 5.1.4 on 2025-04-02 06:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_cart_created_at_alter_cart_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
