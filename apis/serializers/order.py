from rest_framework import serializers
from apis.models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user_profile',
            'total_amount',
            'created_at',
            'payment_method',
            'rc_code_used',
            'sale_code',
        ]
        read_only_fields = ['id', 'created_at', 'user_profile', 'sale_code']
