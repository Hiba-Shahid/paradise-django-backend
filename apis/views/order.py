from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from apis.models.order import Order
from apis.models.user_profile import UserProfile
from apis.models.cart import Cart
from apis.serializers.order import OrderSerializer
import uuid

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer):
        try:
            user_profile = self.request.user.userprofile
        except UserProfile.DoesNotExist:
            raise PermissionDenied("User profile not found.")

        sale_code = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        order = serializer.save(user_profile=user_profile, sale_code=sale_code)

        try:
            active_cart = Cart.objects.get(user_profile=user_profile, status='active')
            active_cart.status = 'closed'
            active_cart.save()
        except Cart.DoesNotExist:
            pass  

        Cart.objects.create(user_profile=user_profile, status='active')