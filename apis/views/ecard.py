from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated  # Optional
from apis.models.ecard import ECard
from apis.serializers.ecard import ECardSerializer

class ECardViewSet(viewsets.ModelViewSet):
    queryset = ECard.objects.all()
    serializer_class = ECardSerializer
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(operation_description="List all e-cards")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve an e-card by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new e-card")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an existing e-card")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete an e-card")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
