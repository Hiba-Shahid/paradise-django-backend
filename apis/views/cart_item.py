from rest_framework import viewsets, permissions
from apis.models.cart_item import CartItem
from apis.serializers.cart_item import CartItemSerializer
from rest_framework.exceptions import PermissionDenied


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()

        if not self.request.user.is_authenticated:
            return CartItem.objects.none()

        return CartItem.objects.filter(cart__user_profile__user=self.request.user)

    def perform_create(self, serializer):
        cart = serializer.validated_data['cart']
        if cart.user_profile.user != self.request.user:
            raise PermissionDenied("You can only add items to your own cart.")
        serializer.save()

