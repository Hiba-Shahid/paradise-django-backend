from rest_framework import viewsets
from apis.models.competition_category import CompetitionCategory
from apis.serializers.competition_category import CompetitionCategorySerializer

class CompetitionCategoryViewSet(viewsets.ModelViewSet):
    queryset = CompetitionCategory.objects.all()
    serializer_class = CompetitionCategorySerializer
