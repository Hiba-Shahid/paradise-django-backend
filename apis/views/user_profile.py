from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apis.models.user_profile import UserProfile
from drf_yasg.utils import swagger_auto_schema
from apis.serializers.user_profile import UserProfileSerializer

class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile  
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")

    @swagger_auto_schema(
        operation_description="Retrieve user profile",
        responses={200: UserProfileSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
