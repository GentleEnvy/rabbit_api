from datetime import datetime

from rest_framework import serializers

from api.models import *

__all__ = [
    'CompleteTaskUpdateSerializer', 'CompleteBunnyJiggingTaskUpdateSerializer',
    'CompleteSlaughterInspectionTaskUpdateSerializer'
]


class CompleteTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completed_at']
        extra_kwargs = {
            'completed_at': {
                'required': False, 'allow_null': False, 'default': datetime.utcnow
            }
        }


class CompleteBunnyJiggingTaskUpdateSerializer(CompleteTaskUpdateSerializer):
    class Meta(CompleteTaskUpdateSerializer.Meta):
        model = BunnyJiggingTask
        fields = CompleteTaskUpdateSerializer.Meta.fields + ['males']
        extra_kwargs = CompleteTaskUpdateSerializer.Meta.extra_kwargs | {
            'males': {'required': True, 'allow_null': False}
        }


class CompleteSlaughterInspectionTaskUpdateSerializer(CompleteTaskUpdateSerializer):
    class Meta(CompleteTaskUpdateSerializer.Meta):
        model = SlaughterInspectionTask
        fields = CompleteTaskUpdateSerializer.Meta.fields + ['weights']
        extra_kwargs = CompleteTaskUpdateSerializer.Meta.extra_kwargs | {
            'weights': {'required': True, 'allow_null': False}
        }
    
    def validate_weights(self, weights):
        self.instance.cleaner.clean_weights(weights)
        return weights
