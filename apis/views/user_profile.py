# from rest_framework import viewsets, permissions
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from apis.models.user_profile import UserProfile
# from apis.serializers.user_profile import UserProfileSerializer


# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return UserProfile.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apis.models.user_profile import UserProfile
from apis.serializers.user_profile import UserProfileSerializer


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        try:
            return self.request.user.profile  # or UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")

    def get(self, request, *args, **kwargs):
        """Handles retrieving the user profile."""
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handles updating user profile details."""
        return super().put(request, *args, **kwargs)
