from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from product.models import Cart


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    old_session_key = request.session['old_session_key']
    if old_session_key:
        session_cart = Cart.objects.filter(session_key=old_session_key).first()
        if session_cart:
            user_cart = Cart.objects.filter(user=user).first()
            print(user_cart)
            if user_cart and user_cart != session_cart:
                session_cart.user = user
                session_cart.save()
                user_cart.delete()
            else:
                session_cart.user = user
                session_cart.save()