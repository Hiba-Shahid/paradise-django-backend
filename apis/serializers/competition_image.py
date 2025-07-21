from rest_framework import serializers
from apis.models.competition_image import CompetitionImage

class CompetitionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionImage
        fields = ['id', 'competition', 'image', 'is_main']
