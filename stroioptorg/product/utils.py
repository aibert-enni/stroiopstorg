from django.db.models import OuterRef, Exists, Q
from rest_framework.pagination import PageNumberPagination

from product.models import AttributeValue, ProductAttribute, Category


def get_nested_categories(categories, parent=None):
    nested = []
    for category in categories:
        if category.parent == parent:
            children = get_nested_categories(categories, parent=category)
            nested.append({
                'id': category.id,
                'name': category.name,
                'url': category.slug,
                'children': children
            })
    return nested

def get_filter(attribute, products):
    return AttributeValue.objects.filter(attribute=attribute, product_attributes__product__in=products).only('value').distinct()

def get_category_filter(category: Category):
    category_filter = Q(category=category)
    # Для всех подкатегорий и их подкатегорий
    subcategories = Category.objects.filter(parent=category)
    category_filter |= Q(category__in=subcategories)

    # Для подкатегорий третьего уровня
    for subcategory in subcategories:
        subsubcategories = Category.objects.filter(parent=subcategory)
        category_filter |= Q(category__in=subsubcategories)

    return category_filter

class ProductListPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'paginate_by'
    max_page_size = 24
