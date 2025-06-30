from rest_framework import serializers
from .models import Product, Collection, Product, Cart, CartItem,  Order, OrderItem, Transaction
from main.models import UserProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'is_active']

class CollectionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'image', 'is_active', 'created_at', 'products']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=UserProfile.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'is_active']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user__username', queryset=UserProfile.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'delivery_address', 'shipping_method', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price_per_item', 'total_price']

class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field='id', queryset=Order.objects.all(), required=False)  # Optional
  

    class Meta:
        model = Transaction
        fields = ['id', 'order', 'competition', 'transaction_id', 'amount', 'payment_method', 'status', 'transaction_type', 'transaction_date']

