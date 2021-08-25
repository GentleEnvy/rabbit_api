from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.exceptions import APIWarning
from api.models import User

__all__ = ['BaseAuthSerializer']


class BaseAuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_('Username'), required=True, allow_null=False
    )
    password = serializers.CharField(
        label=_('Password'), style={'input_type': 'password'}, trim_whitespace=False,
        required=True, allow_null=False
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'), username=username, password=password
        )
        if user is None:
            if User.objects.filter(username=username).exists():
                raise APIWarning('Invalid password', codes=['authorization', 'password'])
            raise APIWarning(
                'User with this username does not exist',
                codes=['authorization', 'username']
            )
        
        attrs['user'] = user
        return attrs
    
    def update(self, instance, validated_data):
        raise NotImplemented
    
    def create(self, validated_data):
        raise NotImplemented
