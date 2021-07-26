from datetime import datetime

from rest_framework import serializers

from api.models import Task

__all__ = ['InProgressTaskUpdateSerializer']


class InProgressTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completed_at', 'males', 'females']
        extra_kwargs = {'completed_at': {'required': False, 'default': datetime.now}}
    
    males = serializers.IntegerField(required=False, allow_null=False)
    females = serializers.IntegerField(required=False, allow_null=False)
    
    weights = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_null=False,
        allow_empty=False
    )
