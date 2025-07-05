from django.db import transaction
from django.db.models import ExpressionWrapper, F, IntegerField, Q, Manager, QuerySet, Prefetch
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from elasticsearch_dsl import Q as dsl_Q

from apps.product.documents import ProductDocument
from apps.product.models import Product, Cart, CartProduct, Category
from utils.common import get_object_by_user_or_session_key, get_objects_by_user_or_session_key


class CartService:
    def __init__(self, request):
        self.request = request

    def get_cart(self) -> Cart:
        cart = Cart.objects.prefetch_related(
            Prefetch('products', queryset=CartProduct.objects.select_related('product__cover'))
        )

        if self.request.user.is_authenticated:
            cart, _ = cart.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            cart, _ = cart.get_or_create(session_key=self.request.session.session_key)

        return cart


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
        # cart_product = self.get_cart_product(self.request, cart_product_id)

        cart_product = CartProduct.objects.select_related('cart', 'product__cover').get(id=cart_product_id)

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
        return get_object_by_user_or_session_key(request, CartProduct, get_by_auth=False, auth_fields=['cart'],
                                                 pk=cart_product_id)

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

        # Getting names of types of products from query params
        if query_params:
            skip_keys = {'order', 'price_from', 'price_to', 'paginate_by', 'page'}
            attributes_ids = [
                query_params.getlist(key)
                for key in query_params if key not in skip_keys
            ]
            # Applying filter by attributes
            for ids in attributes_ids:
                product_filter &= Q(product_attributes__attribute_value__in=ids)

        # Applying the category filter
        products = products.select_related('cover').filter(
            product_filter)

        products = products.distinct().only('id', 'cover', 'name', 'slug', 'sku', 'discount', 'description',
                                            'price', 'cover__image').order_by(order)

        return products


class ProductService:

    @staticmethod
    def search(search_input: str, order: str, price_from: int = None, price_to: int = None, **kwargs) -> QuerySet[
        Product]:
        must_filters = []

        if price_from and price_to:
            must_filters.append(dsl_Q('range', price={'gte': price_from, 'lte': price_to}))
        elif price_from:
            must_filters.append(dsl_Q('range', price={'gte': price_from}))
        elif price_to:
            must_filters.append(dsl_Q('range', price={'lte': price_to}))

        if order:
            sort_field = order.lstrip('-')
            direction = 'desc' if order.startswith('-') else 'asc'
            sort = {
                sort_field: {
                    'order': direction
                }
            }
        else:
            sort = {}

        if search_input:
            products = ProductDocument.search().query("bool",
                                                      should=[
                                                          dsl_Q("match", name={'query': search_input.strip(),
                                                                               'operator': 'and'}),
                                                          dsl_Q("nested", path="product_attributes",
                                                                query=dsl_Q("match",
                                                                            product_attributes__attribute_value={
                                                                                'query': search_input,
                                                                                'operator': 'and'}))
                                                      ], filter=must_filters).sort(sort).to_queryset()
            return products
        else:
            return Product.objects.all()

    @staticmethod
    def get_categories_from_products(products: QuerySet[Product]) -> QuerySet[Category]:
        return Category.objects.filter(products__in=products).distinct()
