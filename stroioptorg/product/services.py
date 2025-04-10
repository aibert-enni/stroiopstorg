from django.db import transaction
from django.db.models import ExpressionWrapper, F, IntegerField, Q, Manager
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from product.models import Product, Cart, CartProduct, Category
from utils.common import get_object_by_user_or_session_key, get_objects_by_user_or_session_key


class CartService:
    def __init__(self, request):
        self.request = request

    @staticmethod
    def get_cart(request):
        return get_object_by_user_or_session_key(request,Cart)

class CartProductService:
    def __init__(self, request):
        self.request = request

    def create(self, product_id, quantity) -> Cart:
        with transaction.atomic():
            product = get_object_or_404(Product, id=product_id)

            # Check stock
            if product.stock_quantity < quantity:
                raise serializers.ValidationError('В складе количество меньше')

            if self.request.user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(user=self.request.user)
            else:
                if not self.request.session.session_key:
                    self.request.session.create()
                cart, _ = Cart.objects.get_or_create(session_key=self.request.session.session_key)

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

            return cart

    def update(self, cart_product_id, quantity) -> CartProduct:
        cart_product = self.get_cart_product(self.request, cart_product_id)

        # get difference between request quantity and quantity from database
        quantity_diff = quantity - cart_product.quantity

        # if quantity in stock less than quantity diff return error
        if cart_product.product.stock_quantity < abs(quantity_diff):
            raise ValidationError('В складе количество меньше')

        with transaction.atomic():
            cart_product.quantity = quantity
            cart_product.save()

        return cart_product

    def delete(self, cart_product_id):
        with transaction.atomic():
            cart_product = self.get_cart_product(self.request, cart_product_id)
            cart_product.delete()

    @staticmethod
    def get_cart_product(request, cart_product_id):
        return get_object_by_user_or_session_key(request, CartProduct, get_by_auth=False, auth_fields=['cart'], pk=cart_product_id)

    @staticmethod
    def get_cart_products(request):
        return get_objects_by_user_or_session_key(request, CartProduct, get_by_auth=False, auth_fields=['cart'])

class ProductByCategoryListService:
    def __init__(self, category):
        self.category = category

    def get_category_filter(self) -> Q:
        category_filter = Q(category=self.category)
        # For all category and subcategories
        subcategories = Category.objects.filter(parent=self.category)
        category_filter |= Q(category__in=subcategories)

        # For subcategory in 3 depth
        for subcategory in subcategories:
            subsubcategories = Category.objects.filter(parent=subcategory)
            category_filter |= Q(category__in=subsubcategories)

        return category_filter

    def get_products(self, price_from=None, price_to=None, order='price', query_params=None) -> Manager:
        products = Product.objects

        # Basic filter for products search in current category
        product_filter = self.get_category_filter()

        # Filter of prices
        # Initialization of discount field
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

        # Applying the category filter
        products = products.prefetch_related('product_attributes__attribute_value', 'cover').filter(
            product_filter)

        # Filter by type of product
        attributes_ids = []

        # Getting names of types of products from query params
        if query_params:
            for param in query_params:
                if param in {'order', 'price_from', 'price_to', 'paginate_by', 'page'}:
                    continue
                attributes_ids.append(query_params.getlist(param))

        # Applying filter by attributes
        for ids in attributes_ids:
            products = products.filter(product_attributes__attribute_value__in=ids)

        products = products.distinct().only('id', 'name', 'slug', 'sku', 'discount', 'description',
                                            'price', ).order_by(order)

        return products