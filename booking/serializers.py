from rest_framework import serializers

from authentication.serializers import ResponseUserSerializer
from .models import Order, OrderItem, Address, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'price', 'image', 'tags', 'is_active')


class ResponseMenuSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    price = serializers.FloatField()
    image = serializers.ImageField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'address', 'total_price')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'quantity', 'product')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'address', 'latitude', 'longitude', 'url')
        extra_kwargs = {
            'url': {'read_only': True}
        }


class ResponseAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    address = serializers.CharField(max_length=250)
    url = serializers.URLField(read_only=True)


class ResponseOrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    quantity = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ResponseMenuSerializer(read_only=True)


class ResponseOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_price = serializers.IntegerField()
    user = ResponseUserSerializer(read_only=True)
    address = ResponseAddressSerializer(read_only=True)
    order_items = ResponseOrderItemSerializer(read_only=True, many=True)


class CreateOrderItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    product = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    address = serializers.IntegerField(min_value=1)
    order_items = CreateOrderItemSerializer(many=True)
