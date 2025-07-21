from rest_framework import viewsets, permissions
from apis.models.affiliate_profile import AffiliateProfile
from apis.serializers.affiliate_profile import AffiliateProfileSerializer


class AffiliateProfileViewSet(viewsets.ModelViewSet):
    queryset = AffiliateProfile.objects.all()
    serializer_class = AffiliateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AffiliateProfile.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)
