from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название региона')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'