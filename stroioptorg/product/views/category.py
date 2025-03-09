from django.db.models import Q, ExpressionWrapper, F, IntegerField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from product.models import Category, Product
from product.serializers import ProductListQuerySerializer, ProductSerializer
from product.utils import get_nested_categories, ProductListPagination, get_filter, get_category_filter


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

        # Базовый фильтр для поиска продуктов по текущей категории
        product_filter = get_category_filter(category)

        # Применяем фильтрацию и возвращаем продукты
        products = Product.objects.filter(product_filter).prefetch_related('cover').only('name', 'slug', 'price',
                                                                                         'discount', 'cover',
                                                                                         'sku').order_by('price')

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


class ProductByCategoryListView(ListAPIView):
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

        products = Product.objects

        # Базовый фильтр для поиска продуктов по текущей категории
        product_filter = get_category_filter(category)

        # Фильтр цен
        # объявляем поле цены со скидкой в sql запросе
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

        # Применяем фильтр категории
        products = products.prefetch_related('product_attributes__attribute_value', 'cover').filter(
            product_filter)

        # Фильтр по типу товара
        attributes_ids = []

        # получаем имена атрибутов с url
        for param in self.request.query_params:
            if param in {'order', 'price_from', 'price_to', 'paginate_by', 'page'}:
                continue
            attributes_ids.append(self.request.query_params.getlist(param))

        # применяем фильтр по атрибутам
        for ids in attributes_ids:
            products = products.filter(product_attributes__attribute_value__in=ids)

        products = products.distinct().only('id', 'name', 'slug', 'sku', 'discount', 'description',
                                            'price', ).order_by(order)

        return products

