from django.core.validators import MinValueValidator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from product.models import Category, Product
from product.pagination import ProductListPagination
from product.serializers import ProductSerializer
from product.services import ProductByCategoryListService
from product.utils import get_nested_categories, get_filter


def get_categories(request):
    categories = Category.objects.all()
    # Получаем дерево категории каталога
    nested_categories = get_nested_categories(categories)
    return JsonResponse(nested_categories, safe=False)

class ProductsByCategoryView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 9
    template_name = 'product/catalog.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')

        category = get_object_or_404(Category, slug=category_slug)

        self.category = category

        products = ProductByCategoryListService(category).get_products()

        self.products = products

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['category'] = self.category

        products = self.products

        filters = {}

        category_filters = self.category.filter_attributes.filter(is_filterable=True).prefetch_related('attribute')

        for category_filter in category_filters:
            filters[category_filter.attribute.filter_name] = {
                'name': category_filter.attribute.name,
                'values': get_filter(category_filter.attribute, products)
            }

        context_data['filters'] = filters

        context_data['total_products'] = self.products.count()

        return context_data


class ProductByCategoryListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    class ProductListQuerySerializer(serializers.Serializer):
        order_types = {'price', '-price', '-created_at'}

        order = serializers.ChoiceField(choices=order_types, default='price')

        price_from = serializers.IntegerField(validators=[MinValueValidator(1)], required=False)
        price_to = serializers.IntegerField(validators=[MinValueValidator(1)], required=False)

    def get_queryset(self):
        query_serializer = self.ProductListQuerySerializer(data=self.request.query_params)

        query_serializer.is_valid(raise_exception=True)

        category_slug = self.kwargs.get('category_slug')
        order = query_serializer.data.get('order')
        price_from = query_serializer.data.get('price_from')
        price_to = query_serializer.data.get('price_to')

        category = get_object_or_404(Category, slug=category_slug)

        products = ProductByCategoryListService(category).get_products(price_from, price_to, order, self.request.query_params)

        return products

