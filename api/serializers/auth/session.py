from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

__all__ = ['AuthSessionSerializer']


class AuthSessionSerializer(AuthTokenSerializer):
    token = serializers.HiddenField(default=None)

    def update(self, instance, validated_data):
        raise AttributeError

    def create(self, validated_data):
        raise AttributeError
