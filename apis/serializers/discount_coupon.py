from rest_framework import serializers
from apis.models.discount_coupon import DiscountCoupon

class DiscountCouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = DiscountCoupon
        fields = [
            'id', 'code', 'percentage', 'is_affiliate_rc',
            'competition', 'usage_limit', 'used_count',
            'active', 'expires_at', 'is_valid'
        ]

    def get_is_valid(self, obj):
        return obj.is_valid()
