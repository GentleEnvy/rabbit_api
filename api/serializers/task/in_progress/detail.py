from datetime import datetime

from rest_framework import serializers

from api.models import *

__all__ = [
    'InProgressTaskUpdateSerializer', 'InProgressBunnyJiggingTaskUpdateSerializer',
    'InProgressSlaughterInspectionTaskUpdateSerializer'
]


class InProgressTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completed_at']
        extra_kwargs = {
            'completed_at': {
                'required': False, 'allow_null': False, 'default': datetime.utcnow
            }
        }


class InProgressBunnyJiggingTaskUpdateSerializer(InProgressTaskUpdateSerializer):
    class Meta(InProgressTaskUpdateSerializer.Meta):
        model = BunnyJiggingTask
        fields = InProgressTaskUpdateSerializer.Meta.fields + ['males', 'females']
        extra_kwargs = InProgressTaskUpdateSerializer.Meta.extra_kwargs | {
            'males': {'required': True, 'allow_null': False},
            'females': {'required': True, 'allow_null': False}
        }


class InProgressSlaughterInspectionTaskUpdateSerializer(InProgressTaskUpdateSerializer):
    class Meta(InProgressTaskUpdateSerializer.Meta):
        model = SlaughterInspectionTask
        fields = InProgressTaskUpdateSerializer.Meta.fields + ['weights']
        extra_kwargs = InProgressTaskUpdateSerializer.Meta.extra_kwargs | {
            'weights': {'required': True, 'allow_null': False}
        }
    
    def validate_weights(self, weights):
        self.instance.clean_weights(weights)
        return weights
