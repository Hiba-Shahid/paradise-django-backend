from rest_framework import viewsets
from apis.models.ecard import ECard
from apis.serializers.ecard import ECardSerializer

class ECardViewSet(viewsets.ModelViewSet):
    queryset = ECard.objects.all()
    serializer_class = ECardSerializer
