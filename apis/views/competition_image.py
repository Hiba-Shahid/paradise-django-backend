from rest_framework import viewsets
from apis.models.competition_image import CompetitionImage
from apis.serializers.competition_image import CompetitionImageSerializer

class CompetitionImageViewSet(viewsets.ModelViewSet):
    queryset = CompetitionImage.objects.all()
    serializer_class = CompetitionImageSerializer
