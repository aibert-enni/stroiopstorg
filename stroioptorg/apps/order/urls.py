from django.urls import path

from order.views import OrderView

app_name = 'order'

urlpatterns = [
    path('order', OrderView.as_view(), name='order'),
]