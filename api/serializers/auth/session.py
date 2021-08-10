from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

__all__ = ['AuthSessionSerializer']


# noinspection PyAbstractClass
class AuthSessionSerializer(AuthTokenSerializer):
    token = serializers.HiddenField(default=None)
