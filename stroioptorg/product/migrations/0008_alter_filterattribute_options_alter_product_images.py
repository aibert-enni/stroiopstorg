# Generated by Django 5.1.4 on 2025-02-11 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_rename_attributes_filterattribute_attribute'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filterattribute',
            options={'verbose_name': 'Атрибут для фильтра', 'verbose_name_plural': 'Атрибуты для фильтров'},
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(null=True, related_name='products', to='product.productimage', verbose_name='Изображения'),
        ),
    ]
