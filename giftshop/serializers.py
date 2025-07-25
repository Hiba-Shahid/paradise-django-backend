from rest_framework import serializers
from .models import Transaction
from apis.models.order import Order


class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(slug_field='id', queryset=Order.objects.all(), required=False)  # Optional
  

    class Meta:
        model = Transaction
        fields = ['id', 'order', 'payment_method', 'status']

