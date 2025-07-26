from rest_framework import viewsets, permissions
from apis.models.product_category import ProductCategory
from apis.serializers.product_category import ProductCategorySerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Show only active categories to non-authenticated users
        if self.request.user.is_authenticated:
            return ProductCategory.objects.all()
        return ProductCategory.objects.filter(is_active=True)
