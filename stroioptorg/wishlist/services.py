from typing import Literal, Union

from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from product.models import Product
from wishlist.models import WishlistProduct


class WishlistService:
    def __init__(self, request: Request):
        self.request = request

    def get_list(self) -> Union[list[Product]]:
        if self.request.user.is_authenticated:
            wishlist = WishlistProduct.objects.filter(user=self.request.user).select_related('product')
            products = [item.product for item in wishlist]
        else:
            wishlist = self.request.session.get('wishlist')
            products = Product.objects.filter(id__in=wishlist)

        return products

    def add_product(self, product_id: int):
        product = get_object_or_404(Product, pk=product_id)

        if self.request.user.is_authenticated:
            WishlistProduct.objects.get_or_create(user=self.request.user, product=product)
        else:
            wishlist = self.request.session.get('wishlist', [])

            if product.id not in wishlist:
                wishlist.append(product.id)
                self.request.session['wishlist'] = wishlist

    def remove_product(self, product_id: int):
        if self.request.user.is_authenticated:
            get_object_or_404(WishlistProduct, pk=product_id, user=self.request.user).delete()
        else:
            wishlist = self.request.session.get('wishlist', [])
            if product_id in wishlist:
                wishlist.remove(product_id)
                self.request.session['wishlist'] = wishlist

    def toggle(self, product_id: int) -> Literal['added', 'removed']:
        status: Literal['added', 'removed']

        product = get_object_or_404(Product, pk=product_id)

        if self.request.user.is_authenticated:
            wishlist_product, created = WishlistProduct.objects.get_or_create(user=self.request.user, product=product)
            if not created:
                wishlist_product.delete()
                status = 'removed'
            else:
                status = 'added'
        else:
            wishlist = self.request.session.get('wishlist', [])
            if product_id in wishlist:
                wishlist.remove(product_id)
                status = 'removed'
            else:
                wishlist.append(product_id)
                status = 'added'
            self.request.session['wishlist'] = wishlist

        return status

    def clear_wishlist(self):
        if self.request.user.is_authenticated:
            WishlistProduct.objects.filter(user=self.request.user).delete()
        else:
            wishlist = self.request.session.get('wishlist', [])
            if len(wishlist) > 0:
                self.request.session['wishlist'] = []

    def check_product(self, product_id: int) -> bool:
        if self.request.user.is_authenticated:
            return WishlistProduct.objects.filter(user=self.request.user, product=product_id).exists()
        else:
            wishlist = self.request.session.get('wishlist', [])
            if product_id in wishlist:
                return True