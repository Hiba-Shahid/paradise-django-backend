from rest_framework import serializers
from apis.models.affiliate_withdrawal import AffiliateWithdrawal


class AffiliateWithdrawalSerializer(serializers.ModelSerializer):
    affiliate_username = serializers.CharField(source='affiliate.user_profile.user.username', read_only=True)

    class Meta:
        model = AffiliateWithdrawal
        fields = [
            'id',
            'affiliate',
            'affiliate_username',
            'amount',
            'approved_at',
            'status',
            'notes',
            'created_at',
        ]
        read_only_fields = ['approved_at', 'status', 'created_at']
