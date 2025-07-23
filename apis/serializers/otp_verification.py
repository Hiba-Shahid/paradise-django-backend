from rest_framework import serializers
from apis.models.otp_verification import OTPVerification

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ['id', 'user_profile', 'code', 'is_verified', 'purpose', 'created_at']
        read_only_fields = ['is_verified', 'created_at', 'updated_at']
