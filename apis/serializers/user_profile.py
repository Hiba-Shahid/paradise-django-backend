from rest_framework import serializers
from django.contrib.auth.models import User
from apis.models.user_profile import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'phone',
            'street',
            'city',
            'province',
            'country',
            'address',
            'updated_at',
            'is_allow_affiliate_marketing',
            'referrar'
        ]
