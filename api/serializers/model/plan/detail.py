from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.services.model.rabbit.filterer import RabbitFilterer
from api.services.model.rabbit.managers import FatteningRabbitManager
from api.models import Plan, FatteningRabbit

__all__ = ['PlanUpdateSerializer']


class PlanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['rabbits']
    
    class _RabbitsField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            queryset = super().get_queryset()
            queryset = queryset.filter(Q(plan=self.parent.parent.instance) | Q(plan=None))
            filterer = RabbitFilterer(queryset)
            filterer.filter(status=[FatteningRabbitManager.STATUS_READY_TO_SLAUGHTER])
            return filterer.queryset
    
    rabbits = _RabbitsField(
        many=True, queryset=FatteningRabbit.objects.all(), source='fatteningrabbit_set'
    )
    
    def validate(self, attrs):
        rabbits = attrs['fatteningrabbit_set']
        plan = self.instance
        if len(rabbits) > plan.quantity:
            raise ValidationError(
                f'Too many rabbits (according to the plan, {plan.quantity} rabbits are '
                f'expected, but {len(rabbits)} have been given)'
            )
        return attrs
