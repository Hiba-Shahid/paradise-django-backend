from rest_framework import viewsets
from apis.models.instant_win_prize import InstantWinPrize
from apis.serializers.instant_win_prize import InstantWinPrizeSerializer

class InstantWinPrizeViewSet(viewsets.ModelViewSet):
    queryset = InstantWinPrize.objects.all()
    serializer_class = InstantWinPrizeSerializer
