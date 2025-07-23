from rest_framework import viewsets, filters
from drf_yasg.utils import swagger_auto_schema
from apis.models.ticket import Ticket
from apis.serializers.ticket import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ticket_number', 'competition__title', 'user__username']
    ordering_fields = ['created_at', 'ticket_number']

    @swagger_auto_schema(operation_description="List all tickets")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a ticket by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new ticket")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an existing ticket")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a ticket")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        # Optional: prevent queryset explosion in Swagger UI
        if getattr(self, 'swagger_fake_view', False):
            return Ticket.objects.none()
        return Ticket.objects.all()
