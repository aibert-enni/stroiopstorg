from django.db import models

from main.models import TimeStampedModel
from users.models import User

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название страны')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

class Region(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название региона')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='regions')

    def __str__(self):
        return f'{self.country} -> {self.name}'

    class Meta:
        unique_together = ('name', 'country')
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название города')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='cities')

    def __str__(self):
        return f'{self.region} -> {self.name}'

    class Meta:
        unique_together = ('name', 'region')
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Address(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True)

    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='addresses')
    street = models.CharField(max_length=255, null=True, blank=True)
    house_number = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True,  blank=True,)
    additional_info = models.TextField(null=True, blank=True)

    @property
    def region(self):
        return self.city.region

    @property
    def country(self):
        return self.region.country

    def __str__(self):
        return f"{self.street}, {self.city.name}, {self.region.name}, {self.country.name}"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'