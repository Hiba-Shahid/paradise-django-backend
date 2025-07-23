from rest_framework import viewsets, permissions
from apis.models.affiliate_transaction import AffiliateTransaction
from apis.serializers.affiliate_transaction import AffiliateTransactionSerializer


class AffiliateTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = AffiliateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
     if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
        return AffiliateTransaction.objects.none()
     return AffiliateTransaction.objects.filter(affiliate__user_profile__user=self.request.user)

