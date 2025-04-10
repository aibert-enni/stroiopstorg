from rest_framework import serializers

from order.models import DeliveryMethod, PaymentMethod, Order

from utils.validators import phone_number_validator, firstname_validator, lastname_validator

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['user', 'stripe_payment_id']

class CreateOrderSerializer(serializers.Serializer):
    delivery_method = serializers.ChoiceField(choices=DeliveryMethod.choices, default=DeliveryMethod.PICKUP)
    delivery_cost = serializers.IntegerField()
    address = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=PaymentMethod.choices, default=PaymentMethod.CARD)
    comments = serializers.CharField()

    firstname = serializers.CharField(required=False, validators=[firstname_validator])
    lastname = serializers.CharField(required=False, validators=[lastname_validator])
    company = serializers.CharField(required=False)
    mail = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, validators=[phone_number_validator])

    def validate(self, data):
        super().validate(data)
        request = self.context.get('request', None)

        if request:
            user = request.user

            if not user.is_authenticated:
                if not data['first_name']:
                    raise serializers.ValidationError('Нужно указать имя')
                if not data['last_name']:
                    raise serializers.ValidationError('Нужно указать фамилию')
                if not data['mail']:
                    raise serializers.ValidationError('Нужно указать почту')
                if not data['phone_number']:
                    raise serializers.ValidationError('Нужно указать номер телефона')
        return data

class OrderRefreshPaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class OrderCalculateDeliveryCostSerializer(serializers.Serializer):
    address = serializers.CharField()

class OrderDeclineSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class OrderConfirmSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()