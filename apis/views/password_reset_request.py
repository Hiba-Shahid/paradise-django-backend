from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apis.models.password_reset_request import PasswordResetRequest
from apis.serializers.password_reset_request import PasswordResetRequestSerializer
from apis.models.user_profile import UserProfile
import uuid

class PasswordResetRequestViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]  # Open for unauthenticated users (reset by email)

    def get_queryset(self):
        return PasswordResetRequest.objects.none()  # Not exposed for list view

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            user_profile = UserProfile.objects.get(user__email=email)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        token = str(uuid.uuid4())
        PasswordResetRequest.objects.create(user_profile=user_profile, token=token)

        return Response({'token': token, 'detail': 'Reset token generated.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='verify')
    def verify_token(self, request):
        token = request.data.get('token')

        try:
            obj = PasswordResetRequest.objects.get(token=token, is_used=False)
        except PasswordResetRequest.DoesNotExist:
            return Response({'detail': 'Invalid or already used token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Token is valid.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='consume')
    def consume_token(self, request):
        token = request.data.get('token')

        try:
            obj = PasswordResetRequest.objects.get(token=token, is_used=False)
        except PasswordResetRequest.DoesNotExist:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        obj.is_used = True
        obj.save()
        return Response({'detail': 'Token marked as used.'}, status=status.HTTP_200_OK)
