from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import CartProduct, Product, Cart
from product.serializers import AddToCartSerializer, CartSerializer, UpdateCartProductSerializer, CartProductSerializer, \
    RemoveCartProductSerializer


class CartView(LoginRequiredMixin, ListView):
    template_name = 'product/cart.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        cart_products = CartProduct.objects.filter(cart__user=self.request.user)
        return cart_products


class CartProductView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        try:
            with transaction.atomic():
                # Get or 404 for product
                product = get_object_or_404(Product, id=product_id)

                # Check stock
                if product.stock_quantity < quantity:
                    return Response({
                        'status': 'error',
                        'message': 'Insufficient stock quantity'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Get or create cart
                cart, _ = Cart.objects.get_or_create(user=request.user)

                # Get or create cart product
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

                # Serialize cart for response
                cart_serializer = CartSerializer(cart)

                return Response({
                    'status': 'success',
                    'message': 'Product added to cart successfully',
                    'cart': cart_serializer.data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            serializer = UpdateCartProductSerializer(data=request.data)

            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            cart_product_id = serializer.validated_data['cart_product_id']
            quantity = serializer.validated_data['quantity']

            cart_product = get_object_or_404(CartProduct, id=cart_product_id, cart__user=self.request.user)

            # get difference between request quantity and quantity from database
            quantity_diff = quantity - cart_product.quantity

            # if quantity in stock less than quantity diff return error
            if cart_product.product.stock_quantity < abs(quantity_diff):
                return Response({
                    'status': 'error',
                    'message': 'Insufficient stock quantity'
                }, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                cart_product.quantity = quantity
                cart_product.save()

                cart_product.product.stock_quantity -= quantity_diff
                cart_product.product.save()

            cart_product_serializer = CartProductSerializer(cart_product)

            return Response({
                'status': 'success',
                'message': 'Cart Product updated successfully',
                'cart': cart_product_serializer.data
            }, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        serializer = RemoveCartProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': serializer.errors
            })

        cart_product_id = serializer.validated_data['cart_product_id']

        try:
            with transaction.atomic():
                cart_product = get_object_or_404(CartProduct, id=cart_product_id)
                cart_product.delete()
                return Response({
                    'status': 'success',
                    'message': 'Cart Product deleted successfully',
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
