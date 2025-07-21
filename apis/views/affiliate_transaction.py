from rest_framework import viewsets, permissions
from apis.models.affiliate_transaction import AffiliateTransaction
from apis.serializers.affiliate_transaction import AffiliateTransactionSerializer


class AffiliateTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = AffiliateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AffiliateTransaction.objects.filter(referrar__user_profile__user=self.request.user)
