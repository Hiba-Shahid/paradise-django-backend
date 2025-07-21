
from rest_framework import serializers
from apis.models.competition_category import CompetitionCategory

class CompetitionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionCategory
        fields = ['id', 'name']
