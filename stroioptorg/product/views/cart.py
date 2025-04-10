from django.views.generic import ListView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from product.serializers import CartSerializer, CartProductSerializer, UpdateCartProductSerializer, \
 AddToCartSerializer
from product.services import CartProductService


class CartView(ListView):
    template_name = 'product/cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        return CartProductService.get_cart_products(self.request)

class CartAPIView(ListAPIView):
    serializer_class = CartProductSerializer

    def get_queryset(self):
        return CartProductService.get_cart_products(self.request)

class CartAddProductAPIView(GenericAPIView):
    serializer_class = AddToCartSerializer

    @extend_schema(
        request=AddToCartSerializer,
        description='Для добавления продукта в корзину'
    )
    def post(self, request):
        query_serializer = self.serializer_class(data=request.data)

        query_serializer.is_valid(raise_exception=True)

        product_id = query_serializer.validated_data['product_id']
        quantity = query_serializer.validated_data['quantity']

        # Serialize cart for response
        cart = CartProductService(request).create(product_id, quantity)

        cart_serializer = CartSerializer(cart)

        return Response({
            'status': 'success',
            'message': 'Продукт был добавлен в корзину удачно',
            'cart': cart_serializer.data
        }, status=status.HTTP_200_OK)

class CartUpdateProductAPIView(GenericAPIView):
    serializer_class = UpdateCartProductSerializer

    @extend_schema(
        request=UpdateCartProductSerializer,
        description='Для обновления количества продуктов в корзине'
    )
    def put(self, request):
        query_serializer = self.serializer_class(data=request.data)

        query_serializer.is_valid(raise_exception=True)

        cart_product_id = query_serializer.validated_data['cart_product_id']
        quantity = query_serializer.validated_data['quantity']

        cart_product = CartProductService(request).update(cart_product_id, quantity)

        cart_product_serializer = CartProductSerializer(cart_product)

        return Response({
            'status': 'success',
            'message': 'Продукт в корзине удачно был обновлен',
            'cart': cart_product_serializer.data
        }, status=status.HTTP_200_OK)

class CartRemoveProductAPIView(GenericAPIView):

    def delete(self, request, pk):
        cart_product_id = pk

        CartProductService(request).delete(cart_product_id)

        return Response({
            'status': 'success',
            'message': 'Продукт был удачно удален с корзины',
        }, status=status.HTTP_204_NO_CONTENT)

