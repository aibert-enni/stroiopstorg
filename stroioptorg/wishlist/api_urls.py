from django.urls import path

from wishlist.views import WishlistAddAPIView, WishlistRemoveAPIView, WishlistToggleAPIView, WishlistListAPIView, \
    WishlistClearAPIView, WishlistCheckProductAPIView

app_name = 'api-wishlist'

urlpatterns = [
    path('wishlist/add/', WishlistAddAPIView.as_view(), name='wishlist-add'),
    path('wishlist/remove/<int:pk>', WishlistRemoveAPIView.as_view(), name='wishlist-remove'),
    path('wishlist/toggle/', WishlistToggleAPIView.as_view(), name='wishlist-toggle'),

    path('wishlist/list/', WishlistListAPIView.as_view(), name='wishlist-list'),
    path('wishlist/clear/', WishlistClearAPIView.as_view(), name='wishlist-clear'),
    path('wishlist/check-product/<int:pk>', WishlistCheckProductAPIView.as_view(), name='wishlist-check-product'),
]