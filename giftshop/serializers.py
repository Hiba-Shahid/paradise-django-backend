from rest_framework import serializers
from .models import Product, Product, Cart, CartItem,  Order, OrderItem, Transaction
from apis.models.user_profile import UserProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'is_active']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=UserProfile.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=UserProfile.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price']

class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field='id', queryset=Order.objects.all(), required=False)  # Optional
  

    class Meta:
        model = Transaction
        fields = ['id', 'order', 'payment_method', 'status']

