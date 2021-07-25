from rest_framework import serializers

from api.models import Task

__all__ = ['WaitingConfirmationTaskUpdateSerializer']


class WaitingConfirmationTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_confirmed']
        extra_kwargs = {'is_confirmed': {'required': True, 'allow_null': False}}
