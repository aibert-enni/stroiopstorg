from django.urls import path

from product.views import CartAPIView, CartAddProductAPIView, CartUpdateProductAPIView, CartRemoveProductAPIView, \
    ProductByCategoryListAPIView

app_name = 'api-product'

urlpatterns = [
    # cart api
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/add/', CartAddProductAPIView.as_view(), name='cart-add-product'),
    path('cart/update/', CartUpdateProductAPIView.as_view(), name='cart-update-product'),
    path('cart/remove/<int:pk>', CartRemoveProductAPIView.as_view(), name='cart-remove-product'),

    # catalog api
    path('catalog/<slug:category_slug>/', ProductByCategoryListAPIView.as_view(), name='catalog-list'),
]