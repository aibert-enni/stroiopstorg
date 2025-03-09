from django.views.generic import DetailView

from product.models import Product, ProductAttribute


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product.html'

    def get_object(self, queryset=None):
        # Применяем select_related что бы не отправлялся два запроса в бд
        product = Product.objects.prefetch_related('images').get(slug=self.kwargs['slug'])
        self.product = product
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attributes = ProductAttribute.objects.filter(product=self.object).select_related(
            'attribute_value__attribute').order_by('attribute_value__attribute__priority')
        context['attributes'] = attributes
        if attributes:
            type_attribute = attributes.first().attribute_value
            similar_products = Product.objects.exclude(pk=self.product.pk).filter(
                product_attributes__attribute_value=type_attribute)
            context['similar_products'] = similar_products
        return context