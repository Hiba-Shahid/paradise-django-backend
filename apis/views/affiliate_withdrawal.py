from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from apis.models.affiliate_withdrawal import AffiliateWithdrawal
from apis.serializers.affiliate_withdrawal import AffiliateWithdrawalSerializer


class AffiliateWithdrawalViewSet(viewsets.ModelViewSet):
    serializer_class = AffiliateWithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AffiliateWithdrawal.objects.filter(affiliate__user_profile__user=self.request.user)

    def perform_create(self, serializer):
        affiliate_profile = self.request.user.profile.affiliate
        serializer.save(affiliate=affiliate_profile)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        withdrawal = self.get_object()
        withdrawal.status = 'approved'
        withdrawal.approved_at = timezone.now()
        withdrawal.save()
        return Response({'detail': 'Withdrawal approved.'}, status=status.HTTP_200_OK)
