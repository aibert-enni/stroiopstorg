from django.urls import path

from product import views
from product.views import ProductsByCategoryView, ProductDetailView, CartView, CartProductView, \
    ProductByCategoryListView

app_name = 'product'

urlpatterns = [
    path('catalog/tree', views.get_categories, name='catalog-tree'),
    path('catalog/<slug:category_slug>/', ProductsByCategoryView.as_view(), name='catalog'),
    path('catalog/api/<slug:category_slug>/', ProductByCategoryListView.as_view(), name='catalog-list'),
    path('catalog/product/<slug:slug>/', ProductDetailView.as_view(), name='catalog-product'),
    path('catalog/cart/create/', CartProductView.as_view(), name='cart_create'),
    path('catalog/cart/update/', CartProductView.as_view(), name='cart_update'),
    path('catalog/cart', CartView.as_view(), name='cart'),
]
