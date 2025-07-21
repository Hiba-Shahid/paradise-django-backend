from rest_framework import serializers
from apis.models.affiliate_profile import AffiliateProfile
from apis.serializers.user_profile import UserProfileSerializer


class AffiliateProfileSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = AffiliateProfile
        fields = [
            'id',
            'user_profile',
            'rc_code',
            'affiliate_joined_on',
            'total_earnings',
        ]
        read_only_fields = ['rc_code', 'total_earnings']
