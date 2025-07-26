from rest_framework import viewsets, permissions
from apis.models.cart import Cart
from apis.serializers.cart import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()  

        return Cart.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)

