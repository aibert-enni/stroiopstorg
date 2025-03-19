from rest_framework import serializers

from product.models import CartProduct, Cart, Product


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


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'quantity', 'subtotal']

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_amount', 'products']



