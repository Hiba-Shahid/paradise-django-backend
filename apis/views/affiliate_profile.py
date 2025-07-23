from rest_framework import viewsets, permissions
from apis.models.affiliate_profile import AffiliateProfile
from apis.serializers.affiliate_profile import AffiliateProfileSerializer


class AffiliateProfileViewSet(viewsets.ModelViewSet):
    queryset = AffiliateProfile.objects.all()
    serializer_class = AffiliateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
    # Prevent querying when user is anonymous or schema generation is triggered
     if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
        return AffiliateProfile.objects.none()  # Return an empty queryset
     return AffiliateProfile.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)
