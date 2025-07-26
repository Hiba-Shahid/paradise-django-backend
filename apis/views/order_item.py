from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from apis.models.order_item import OrderItem
from apis.serializers.order_item import OrderItemSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return OrderItem.objects.none()
        return OrderItem.objects.filter(order__user_profile__user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        if order.user_profile.user != self.request.user:
            raise PermissionDenied("You can only add items to your own orders.")
        serializer.save()
