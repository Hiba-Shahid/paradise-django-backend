from rest_framework import serializers
from apis.models.competition import Competition

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'

    def validate_code(self, value):
        if value == "":
            return None
        return value

    def create(self, validated_data):
        # If code is not provided or is blank, it will be handled in model.save()
        return super().create(validated_data)
