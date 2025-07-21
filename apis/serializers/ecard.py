from rest_framework import serializers
from apis.models.ecard import ECard

class ECardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECard
        fields = '__all__'
