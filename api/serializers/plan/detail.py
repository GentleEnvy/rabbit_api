from rest_framework import serializers

from api.managers import FatteningRabbitManager
from api.models import Plan, FatteningRabbit
from api.services.filterers import RabbitFilterer

__all__ = ['PlanUpdateSerializer']


class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['rabbits']
    
    class _RabbitsField(serializers.PrimaryKeyRelatedField):
        def __init__(self, **kwargs):
            super().__init__(
                **kwargs, many=True, queryset=FatteningRabbit.objects.filter(
                    current_type=FatteningRabbit.CHAR_TYPE
                ), source='fatteningrabbit_set'
            )
        
        def get_queryset(self):
            queryset = super().get_queryset()
            filterer = RabbitFilterer(queryset)
            filterer.filter(status=[FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER])
            return filterer.queryset
    
    rabbits = _RabbitsField(write_only=True)
