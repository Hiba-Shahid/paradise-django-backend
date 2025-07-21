from rest_framework import viewsets
from apis.models.winner import Winner
from apis.serializers.winner import WinnerSerializer

class WinnerViewSet(viewsets.ModelViewSet):
    queryset = Winner.objects.all()
    serializer_class = WinnerSerializer
