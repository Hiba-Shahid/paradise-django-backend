from rest_framework import serializers
from apis.models.cart import Cart
from apis.models.product import Product
from apis.models.ticket import Ticket
from apis.models.cart_item import CartItem  

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'ticket', 'quantity']
