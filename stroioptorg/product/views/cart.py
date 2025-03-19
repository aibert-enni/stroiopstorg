from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import CartProduct
from product.serializers import CartSerializer,  CartProductSerializer
from product.services import CartProductService


class CartView(LoginRequiredMixin, ListView):
    template_name = 'product/cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        cart_products = CartProduct.objects.filter(cart__user=self.request.user)
        return cart_products


class CartProductView(APIView):
    permission_classes = (IsAuthenticated,)

    class AddToCartSerializer(serializers.Serializer):
        product_id = serializers.IntegerField(required=True)
        quantity = serializers.IntegerField(required=True, min_value=1)

    class UpdateCartProductSerializer(serializers.Serializer):
        cart_product_id = serializers.IntegerField(required=True)
        quantity = serializers.IntegerField(required=True, min_value=1)

    class RemoveCartProductSerializer(serializers.Serializer):
        cart_product_id = serializers.IntegerField(required=True)

    def post(self, request):
        query_serializer = self.AddToCartSerializer(data=request.data)

        query_serializer.is_valid(raise_exception=True)

        product_id = query_serializer.validated_data['product_id']
        quantity = query_serializer.validated_data['quantity']

        # Serialize cart for response
        cart = CartProductService(request.user).create(product_id, quantity)

        cart_serializer = CartSerializer(cart)

        return Response({
            'status': 'success',
            'message': 'Product added to cart successfully',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)


    def put(self, request):
        query_serializer = self.UpdateCartProductSerializer(data=request.data)

        query_serializer.is_valid(raise_exception=True)

        cart_product_id = query_serializer.validated_data['cart_product_id']
        quantity = query_serializer.validated_data['quantity']

        cart_product = CartProductService(request.user).update(cart_product_id, quantity)

        cart_product_serializer = CartProductSerializer(cart_product)

        return Response({
            'status': 'success',
            'message': 'Cart Product updated successfully',
            'cart': cart_product_serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        query_serializer = self.RemoveCartProductSerializer(data=request.data)

        query_serializer.is_valid(raise_exception=True)

        cart_product_id = query_serializer.validated_data['cart_product_id']

        CartProductService(request.user).delete(cart_product_id)

        return Response({
            'status': 'success',
            'message': 'Cart Product deleted successfully',
        }, status=status.HTTP_200_OK)

