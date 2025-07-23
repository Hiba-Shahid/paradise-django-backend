from rest_framework import viewsets, filters
from drf_yasg.utils import swagger_auto_schema
from apis.models.instant_win_prize import InstantWinPrize
from apis.serializers.instant_win_prize import InstantWinPrizeSerializer

class InstantWinPrizeViewSet(viewsets.ModelViewSet):
    queryset = InstantWinPrize.objects.all()
    serializer_class = InstantWinPrizeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'competition__title']
    ordering_fields = ['created_at', 'name']

    @swagger_auto_schema(operation_description="List all instant win prizes")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve an instant win prize by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new instant win prize")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an existing instant win prize")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete an instant win prize")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return InstantWinPrize.objects.none()
        return InstantWinPrize.objects.all()
