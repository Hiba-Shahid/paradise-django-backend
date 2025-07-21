from rest_framework import serializers
from apis.models.password_reset_request import PasswordResetRequest

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = ['id', 'user_profile', 'token', 'is_used', 'created_at', 'updated_at']
        read_only_fields = ['is_used', 'created_at', 'updated_at']
