from rest_framework import viewsets
from apis.models.competition import Competition
from apis.serializers.competition import CompetitionSerializer

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
