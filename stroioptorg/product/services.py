from django.db import transaction
from django.db.models import ExpressionWrapper, F, IntegerField, Q, Manager
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from product.models import Product, Cart, CartProduct, Category


class CartProductService:
    def __init__(self, user):
        self.user = user

    def create(self, product_id, quantity) -> Cart:
        with transaction.atomic():
            product = get_object_or_404(Product, id=product_id)

            # Check stock
            if product.stock_quantity < quantity:
                raise serializers.ValidationError('Insufficient stock quantity')

            cart, _ = Cart.objects.get_or_create(user=self.user)

            cart_product, created = CartProduct.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': quantity
                }
            )

            if not created:
                cart_product.quantity += quantity
                cart_product.save()

            # Update product stock
            product.stock_quantity -= quantity
            product.save()
            return cart

    def update(self, cart_product_id, quantity) -> CartProduct:
        cart_product = get_object_or_404(CartProduct, id=cart_product_id, cart__user=self.user)

        # get difference between request quantity and quantity from database
        quantity_diff = quantity - cart_product.quantity

        # if quantity in stock less than quantity diff return error
        if cart_product.product.stock_quantity < abs(quantity_diff):
            raise serializers.ValidationError('Insufficient stock quantity')

        with transaction.atomic():
            cart_product.quantity = quantity
            cart_product.save()

            cart_product.product.stock_quantity -= quantity_diff
            cart_product.product.save()

        return cart_product

    def delete(self, cart_product_id):
        with transaction.atomic():
            cart_product = get_object_or_404(CartProduct, id=cart_product_id)
            cart_product.delete()

class ProductByCategoryListService:
    def __init__(self, category):
        self.category = category

    def get_category_filter(self):
        category_filter = Q(category=self.category)
        # Для всех подкатегорий и их подкатегорий
        subcategories = Category.objects.filter(parent=self.category)
        category_filter |= Q(category__in=subcategories)

        # Для подкатегорий третьего уровня
        for subcategory in subcategories:
            subsubcategories = Category.objects.filter(parent=subcategory)
            category_filter |= Q(category__in=subsubcategories)

        return category_filter

    def get_products(self, price_from=None, price_to=None, order='price', query_params=None) -> Manager:

        products = Product.objects

        # Базовый фильтр для поиска продуктов по текущей категории
        product_filter = self.get_category_filter()

        # Фильтр цен
        # объявляем поле цены со скидкой в sql запросе
        if price_from or price_to:
            products = products.annotate(
                discounted_price=ExpressionWrapper(
                    F("price") - (F("price") * (F("discount") * 0.01)),
                    output_field=IntegerField()
                )
            )

        if price_from:
            product_filter &= Q(discounted_price__gte=price_from)

        if price_to:
            product_filter &= Q(discounted_price__lte=price_to)

        # Применяем фильтр категории
        products = products.prefetch_related('product_attributes__attribute_value', 'cover').filter(
            product_filter)

        # Фильтр по типу товара
        attributes_ids = []

        # получаем имена атрибутов с url
        if query_params:
            for param in query_params:
                if param in {'order', 'price_from', 'price_to', 'paginate_by', 'page'}:
                    continue
                attributes_ids.append(query_params.getlist(param))

        # применяем фильтр по атрибутам
        for ids in attributes_ids:
            products = products.filter(product_attributes__attribute_value__in=ids)

        products = products.distinct().only('id', 'name', 'slug', 'sku', 'discount', 'description',
                                            'price', ).order_by(order)

        return products