import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404

from order.models import PaymentStatus, Order, OrderStatus


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = settings.STRIPE_ENDPOINT_KEY

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    session = event['data']['object']
    session_id = session.get('id')

    if session_id:
        try:
            order = get_object_or_404(Order, stripe_payment_id=session_id)
            order.user.cart.get().products.all().delete()

            if event['type'] == 'checkout.session.completed':
                order.payment_status = PaymentStatus.SUCCESS
                order.status = OrderStatus.PROCESSING
            else:
                order.payment_status = PaymentStatus.FAILED
                order.status = OrderStatus.CANCELLED
            order.save()
        except Order.DoesNotExist:
            print(f"❌ Ошибка: Заказ с session_id {session_id} не найден!")

    return HttpResponse(status=200)