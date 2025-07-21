from rest_framework import serializers
from apis.models.winner import Winner

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = '__all__'
