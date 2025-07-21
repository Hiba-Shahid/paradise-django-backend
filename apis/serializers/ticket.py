from rest_framework import serializers
from apis.models.ticket import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_number', 'competition']
