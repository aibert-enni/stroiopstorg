from django.core.validators import MinValueValidator
from django.db import models

from core.models import TimeStampedModel
from users.models import User


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')

    @property
    def total_amount(self):
        return sum(product.subtotal for product in self.products.all())

    def __str__(self):
        return f'{self.id}: {self.user}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartProduct(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products', verbose_name='Корзина')
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='cart_products', verbose_name='Товар')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')

    @property
    def subtotal(self):
        return self.quantity * self.product.price


    class Meta:
        unique_together = ['cart', 'product']
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзин'