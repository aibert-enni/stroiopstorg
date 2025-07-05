from rest_framework import serializers


class WishlistAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class WishlistToggleSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class WishlistToggleResponseSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['added', 'removed'])
    product_id = serializers.IntegerField()

class WishlistCheckProductResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    product_id = serializers.IntegerField()