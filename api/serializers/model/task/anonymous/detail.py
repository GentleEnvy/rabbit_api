from rest_framework import serializers

from api.models import *

__all__ = ['AnonymousTaskUpdateSerializer']


class AnonymousTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user']
        extra_kwargs = {'user': {'required': True}}
    
    def update(self, instance, validated_data):
        user = validated_data['user']
        instance.user = user
        instance.save()
        return instance
