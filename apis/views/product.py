from rest_framework import viewsets, permissions
from apis.models.product import Product
from apis.serializers.product import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.all()
        return Product.objects.filter(is_active=True)
