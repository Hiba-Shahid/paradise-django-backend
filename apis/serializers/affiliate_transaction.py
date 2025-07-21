from rest_framework import serializers
from apis.models.affiliate_transaction import AffiliateTransaction


class AffiliateTransactionSerializer(serializers.ModelSerializer):
    referrar_username = serializers.CharField(source='referrar.user_profile.user.username', read_only=True)
    related_order_code = serializers.CharField(source='related_order.unique_sale_code', read_only=True)

    class Meta:
        model = AffiliateTransaction
        fields = [
            'id',
            'referrar',
            'referrar_username',
            'withdrawal_request',
            'value',
            'transaction_type',
            'related_order',
            'related_order_code',
            'created_at',
        ]
