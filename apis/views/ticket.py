from rest_framework import viewsets
from apis.models.ticket import Ticket
from apis.serializers.ticket import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

