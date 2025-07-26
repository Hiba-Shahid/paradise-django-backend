from rest_framework import serializers
from apis.models.order_item import OrderItem
from apis.serializers.product import ProductSerializer
from apis.serializers.ticket import TicketSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'ticket', 'price']
