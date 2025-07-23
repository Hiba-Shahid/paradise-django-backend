from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apis.models.ticket import Ticket
from apis.serializers.ticket import TicketSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

letter_param = openapi.Parameter(
    'letter', openapi.IN_QUERY,
    description="Starting letter of ticket_number (e.g., A, B, C...)",
    type=openapi.TYPE_STRING
)

@swagger_auto_schema(
    method='get',
    manual_parameters=[letter_param],
    responses={200: TicketSerializer(many=True)}
)
@api_view(['GET'])
def tickets_by_letter(request, competition_id):
    letter = request.query_params.get('letter')

    if not letter or not letter.isalpha() or len(letter) > 2:
        return Response({'error': 'Invalid or missing letter'}, status=status.HTTP_400_BAD_REQUEST)

    tickets = Ticket.objects.filter(
        competition_id=competition_id,
        ticket_number__startswith=letter.upper()
    )

    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
