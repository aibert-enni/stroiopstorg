from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from product.serializers import ProductSerializer
from wishlist.serializers import WishlistAddSerializer, WishlistToggleSerializer, WishlistToggleResponseSerializer, \
    WishlistCheckProductResponseSerializer
from wishlist.services import WishlistService


class WishlistListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return WishlistService(self.request).get_list()

class WishlistAddAPIView(APIView):

    @extend_schema(
        request=WishlistAddSerializer,
        description='Добавляем товар в желаемое, если пользователь авторизован в базу данные, если нет, то сохраняем в сессии'
    )
    def post(self, request):
        add_serializer = WishlistAddSerializer(data=request.data)
        add_serializer.is_valid(raise_exception=True)

        WishlistService(request).add_product(add_serializer.validated_data['product_id'])

        return Response('Товар добавлен в список желаемого', status=status.HTTP_201_CREATED)

class WishlistRemoveAPIView(APIView):

    @extend_schema(
        description='Удаляем товар из списка желаемого'
    )
    def delete(self, request, pk):
        WishlistService(request).remove_product(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistToggleAPIView(APIView):

    @extend_schema(
        request=WishlistToggleSerializer,
        responses=WishlistToggleResponseSerializer,
        description='Что бы по одному запросу либо удалить либо добавить товар в список желаемого'
    )
    def post(self, request):
        toggle_serializer = WishlistToggleSerializer(data=request.data)
        toggle_serializer.is_valid(raise_exception=True)

        product_id = toggle_serializer.validated_data['product_id']

        wishlist_status = WishlistService(request).toggle(product_id)

        return Response({'status': wishlist_status, 'product_id': product_id}, status=status.HTTP_200_OK)

class WishlistClearAPIView(APIView):

    @extend_schema(
        description='Очистка списка желаемого'
    )
    def get(self, request):
        WishlistService(request).clear_wishlist()
        return Response(status=status.HTTP_200_OK)

class WishlistCheckProductAPIView(APIView):

    extend_schema(
        responses=WishlistCheckProductResponseSerializer,
        description='Проверяем есть ли продукт в списке желаемого'
    )
    def get(self, request, pk):
        product_status = WishlistService(request).check_product(pk)
        return Response({'status': product_status, 'product_id': pk}, status=status.HTTP_200_OK)