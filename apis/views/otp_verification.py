from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apis.models.otp_verification import OTPVerification
from apis.serializers.otp_verification import OTPVerificationSerializer
from apis.models.user_profile import UserProfile

class OTPVerificationViewSet(viewsets.ModelViewSet):
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
     if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
         return OTPVerification.objects.none()
     return OTPVerification.objects.filter(user_profile__user=self.request.user)


    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)

    @action(detail=False, methods=['post'], url_path='verify', permission_classes=[permissions.IsAuthenticated])
    def verify_otp(self, request):
        code = request.data.get('code')
        purpose = request.data.get('purpose', 'registration')
        user_profile = request.user.profile

        try:
            otp = OTPVerification.objects.get(user_profile=user_profile, code=code, purpose=purpose, is_verified=False)
        except OTPVerification.DoesNotExist:
            return Response({'detail': 'Invalid or already used OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_verified = True
        otp.save()

        return Response({'detail': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
