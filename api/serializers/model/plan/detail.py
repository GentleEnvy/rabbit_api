from rest_framework import serializers

from api.services.model.rabbit.filterer import RabbitFilterer
from api.services.model.rabbit.managers import FatteningRabbitManager
from api.models import Plan, FatteningRabbit

__all__ = ['PlanUpdateSerializer']

_filterer = RabbitFilterer(FatteningRabbit.objects.all())
_filterer.filter(status=[FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER])


class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['rabbits']
    
    rabbits = serializers.PrimaryKeyRelatedField(
        many=True, queryset=_filterer.queryset, source='fatteningrabbit_set'
    )
