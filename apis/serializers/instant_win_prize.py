from rest_framework import serializers
from apis.models.instant_win_prize import InstantWinPrize

class InstantWinPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstantWinPrize
        fields = '__all__'
