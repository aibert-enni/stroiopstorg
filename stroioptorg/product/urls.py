from django.urls import path

from product import views
from product.views import ProductsByCategoryView, ProductDetailView, CartView

app_name = 'product'

urlpatterns = [
    # catalog
    path('catalog/tree', views.get_categories, name='catalog-tree'),
    path('catalog/<slug:category_slug>/', ProductsByCategoryView.as_view(), name='catalog'),
    path('catalog/product/<slug:slug>/', ProductDetailView.as_view(), name='catalog-product'),

    # cart
    path('cart', CartView.as_view(), name='cart'),


]
