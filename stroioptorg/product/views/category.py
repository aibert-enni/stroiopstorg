from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from product.models import Category, Product
from product.pagination import ProductListPagination
from product.serializers import ProductSerializer, ProductListQuerySerializer
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

@extend_schema(
    parameters=[ProductListQuerySerializer],
    description='Получаем каталог товаров по slug с фильтрами, еще можно делать фильтр с помощью атрибутов товара'
)
class ProductByCategoryListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        query_serializer = ProductListQuerySerializer(data=self.request.query_params)

        query_serializer.is_valid(raise_exception=True)

        category_slug = self.kwargs.get('category_slug')
        order = query_serializer.data.get('order')
        price_from = query_serializer.data.get('price_from')
        price_to = query_serializer.data.get('price_to')

        category = get_object_or_404(Category, slug=category_slug)

        products = ProductByCategoryListService(category).get_products(price_from, price_to, order, self.request.query_params)

        return products

