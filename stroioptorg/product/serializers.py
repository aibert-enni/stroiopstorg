from django.core.validators import MinValueValidator
from rest_framework import serializers

from product.models import CartProduct, Cart, Product, Category


# Product serializers

class ProductSerializer(serializers.ModelSerializer):
    get_discount_price = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'sku', 'discount', 'description', 'price', 'get_discount_price', 'cover_url']

    def get_discount_price(self, obj):
        return obj.discount_price

    def get_cover_url(self, obj):
        if obj.cover:
            return obj.cover.image.url
        return None

class ProductListSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)


class ProductListQuerySerializer(serializers.Serializer):
    order_types = {'price', '-price', '-created_at'}

    order = serializers.ChoiceField(choices=order_types, default='price')

    price_from = serializers.IntegerField(validators=[MinValueValidator(1)], required=False)
    price_to = serializers.IntegerField(validators=[MinValueValidator(1)], required=False)


# Cart serializers

class UpdateCartProductSerializer(serializers.Serializer):
    cart_product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)

class RemoveCartProductSerializer(serializers.Serializer):
    cart_product_id = serializers.IntegerField(required=True)

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_amount', 'products']

# Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

# Search
class SearchQuerySerializer(serializers.Serializer):
    order_types = {'price', '-price', '-created_at'}

    search = serializers.CharField(required=True)
    price_from = serializers.IntegerField(validators=[MinValueValidator(1)], required=False)
    price_to = serializers.IntegerField(validators=[MinValueValidator(1)], required=False)
    order = serializers.ChoiceField(choices=order_types, default='price')



