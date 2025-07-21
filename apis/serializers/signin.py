from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return {'token': token.key}
        raise serializers.ValidationError("Invalid username or password")
