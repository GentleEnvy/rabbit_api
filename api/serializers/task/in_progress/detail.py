from datetime import datetime

from rest_framework import serializers

from api.models import Task

__all__ = ['InProgressTaskUpdateSerializer']


class InProgressTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completed_at']
        extra_kwargs = {'completed_at': {'required': False, 'default': datetime.now}}
