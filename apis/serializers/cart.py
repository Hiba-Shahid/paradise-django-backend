from rest_framework import serializers
from apis.models.cart import Cart
from apis.serializers.user_profile import UserProfileSerializer 

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user_profile', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
        user_profile = UserProfileSerializer(read_only=True)

